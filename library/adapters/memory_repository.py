import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash
from library.adapters import jsondatareader

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Author, Book,Publisher,BooksInventory, ReadingList, User, Review, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader
from tqdm import tqdm

class MemoryRepository(AbstractRepository):
    # books ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__books_inventory = BooksInventory()
        self.__users = list()
        self.__reviews = list()
        self.__authors = list()
        self.__publishers = list()

    def __iter__(self):
        self._current = 0
        return self
    
    def __next__(self):
        if self._current >= len(self.__books_inventory):
            raise StopIteration
        else:
            self._current +=1
            return self.__books_inventory.all_books[self._current-1]

    def __len__(self):
        return len(self.__books_inventory)

########################################        Users

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name = None) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

########################################        Books

    def add_book(self, book: Book):
        try:
            self.__books_inventory.add_book(book)
            for authors in book.authors:
                self.add_author(authors)
            self.add_publisher(book.publisher)
        except ValueError:
            pass

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self.__books_inventory.find_book(id)
        except KeyError:
            pass  # Ignore exception and return None.
        return book    

    def get_number_of_books(self) -> int:
        return len(self.__books_inventory)

    def get_first_book(self):
        book = None

        if len(self.__books_inventory) > 0:
            book = self.__books_inventory.all_books[0]
        return book

    def get_last_book(self):
        book = None

        if len(self.__books_inventory) > 0:
            book = self.__books_inventory.all_books[-1]
        return book
    
    def get_book_by_id(self,id:int): #This is just for clarity's sake on the search side
        return self.get_book(id)
    
    def get_books_by_author_name(self,author_name: str):
        matching_books = list()
        try:
            for book in self.__books_inventory.all_books:
                for authors in book.authors:
                    if author_name.lower() == authors.full_name.lower():
                        matching_books.append(book)
                        break
        except Exception:
            # No books for specified author. Simply return an empty list.
            pass

        return matching_books

    def get_books_by_author_id(self,author_id: int):
        matching_books = list()
        try:
            for book in self.__books_inventory.all_books:
                for authors in book.authors:
                    if author_id == authors.unique_id:
                        matching_books.append(book)
                        break
        except ValueError:
            # No books for specified author. Simply return an empty list.
            pass

        return matching_books

    def get_book_by_release_year(self, target_date: int) -> List[Book]:
        matching_books = list()
        try:
            for book in self.__books_inventory.all_books:
                if book.release_year == target_date:
                    matching_books.append(book)
                else:
                    break
        except ValueError:
            # No books for specified date. Simply return an empty list.
            pass

        return matching_books

    def get_books_by_release_year(self,year):
        matching_books = list()
        try:
            if year == "":
                year = None
            for book in self.__books_inventory.all_books:
                if year == book.release_year:
                    matching_books.append(book)
        except ValueError:
            # No books for specified author. Simply return an empty list.
            pass

        return matching_books

    def get_book_by_title_specific(self,title:str):
        matching_books = list()
        try:
            for book in self.__books_inventory.all_books:
                if title.lower() == book.title.lower():
                    matching_books.append(book)
        except Exception:
            pass

        return matching_books

    def get_book_by_title_general(self,title:str):
        matching_books = list()
        try:
            for book in self.__books_inventory.all_books:
                if title.lower() in book.title.lower():
                    matching_books.append(book)
        except Exception:
            pass

        return matching_books

    def get_books_by_publisher_name(self,publisher_name:str):
        matching_books = list()
        try:
            for book in self.__books_inventory.all_books:
                if publisher_name == book.publisher.name:
                    matching_books.append(book)
        except ValueError:
            # No books for specified author. Simply return an empty list.
            pass

        return matching_books
    
    def get_all_books(self):
        return self.__books_inventory.all_books
########################################        Reviews

    def add_review(self, review: Review):
        review.user_associated.add_review(review)
        self.__reviews.append(review)
        review.book.add_review(review)

    def get_reviews(self):
        return self.__reviews

########################################        Recommendations

    def get_recommendations(self,user_name=None,no_of_books = 10):
        if isinstance(user_name,str):
            user = self.get_user(user_name)
            if user == None:
                
                return self.__books_inventory.get_random_books(no_of_books)
            else:
                
                recommendations = self.__find_recommendations(user.reading_list)
                # print(recommendations)
                if len(recommendations) < no_of_books:
                    return recommendations + self.__books_inventory.get_random_books(no_of_books-len(recommendations))
                elif len(recommendations)>= no_of_books:
                    return recommendations[0:10]
        else:
            return self.__books_inventory.get_random_books(no_of_books)
        
    def __find_recommendations(self,reading_list):
        return_list = {}
        for book_id in reading_list:
            books = self.get_book_by_id(book_id)
            # print(books)
            # print(book_id)
            for authors in books.authors:
                for book in self.get_books_by_author_id(authors.unique_id):
                    if book.book_id not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=4
                        else:
                            return_list[book.book_id] = [book,1]
            
            if books.release_year != None:
                for book in self.get_book_by_release_year(books.release_year):
                    if book.book_id not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=1
                        else:
                            return_list[book.book_id] = [book,1]
                for book in self.get_book_by_release_year(books.release_year-1):
                    if book.book_id not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=1
                        else:
                            return_list[book.book_id] = [book,1]
                for book in self.get_book_by_release_year(books.release_year+1):
                    if book.book_id not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=1
                        else:
                            return_list[book.book_id] = [book,1]
            for book in self.get_books_by_publisher_name(books.publisher.name):
                if book.book_id not in reading_list:
                    if book.book_id in return_list:
                        return_list[book.book_id][1]+=2
                    else:
                        return_list[book.book_id] = [book,1]
        return [self.get_book_by_id(item[0]) for item in sorted(return_list.items(),key=lambda x: x[1][1])]

########################################        Authors and Publishers
    
    def add_author(self,author:Author):
        if isinstance(author,Author):
            if len(self.__authors) == 0 or author not in self.__authors:
                self.__authors.append(author)
    
    def get_author_names(self):
        if len(self.__authors) != 0:
            return [author.full_name for author in self.__authors]
        else:
            return []
    
    def get_author_ids(self):
        if len(self.__authors) != 0:
            return [author.unique_id for author in self.__authors]
        else:
            return []
    
    def add_publisher(self,publisher:Publisher):
        if isinstance(publisher,Publisher):
            if len(self.__publishers) == 0 or publisher not in self.__publishers:
                self.__publishers.append(publisher)

    def get_all_publisher_names(self):
        if len(self.__publishers) != 0:
            return [publisher.name for publisher in self.__publishers]
        else:
            return []


########################################        Reading List

    def get_reading_list_for_user(self,user_name=None):
        user = self.get_user(user_name)
        if user:
            return user.reading_list
        else:
            return self.recommendations(None)
    
    def add_book_to_reading_list(self,user:User,book:Book):
        if isinstance(book,Book) and isinstance(user,User):
            user.add_book_to_reading_list(book.book_id)


def read_json_file(books_file_name:str,authors_file_name:str):
    json_reader = BooksJSONReader(books_file_name,authors_file_name)
    json_reader.read_json_files()

    return json_reader.dataset_of_books

def read_csv_file(filename: str):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row
    
def populate(repo: MemoryRepository,data_path:str="library\\adapters"):
    # Load books and tags into the repository.
    print("Loading Books")
    for books in tqdm(read_json_file(books_file_name=data_path+"\\data\\books.json",authors_file_name=data_path+"\\data\\authors.json")):
        repo.add_book(books)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
    print("Loading Complete")

def load_users(data_path: str, repo: MemoryRepository):
    users = []
    print("Loading Users")
    users_filename = data_path + "\\data\\users.csv"
    
    for data_row in tqdm(read_csv_file(users_filename)):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users.append(user)
    return users

def load_reviews(data_path: str, repo: MemoryRepository, users):
    print("Loading Reviews")
    reviews_filename = data_path + "\\data\\reviews.csv"
    for data_row in tqdm(read_csv_file(reviews_filename)):
        for user in users:
            if user.user_name == data_row[2]:
                temp_user = user
                break
        
        new_review = Review(
            book=repo.get_book_by_id(int(data_row[1])),
            review_text=data_row[3],
            rating=int(data_row[4]),
            review_id=int(data_row[0]),
            user=temp_user,
            timestamp=datetime.fromisoformat(data_row[5])
        )

        repo.add_review(new_review)




