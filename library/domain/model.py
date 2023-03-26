from bisect import insort_left
import datetime
from random import choice, choices
import re
class Author:
    def __init__(self,author_id,author_full_name) -> None:
        self.__author_full_name = None
        self.__unique_id = None
        self.coauthors = []
        self.full_name = author_full_name
        self.__books = []
        if type(author_id) is int and author_id >= 0:
            self.__unique_id = author_id
        else:
            raise ValueError
        
    @property
    def full_name(self):
        return self.__author_full_name

    @full_name.setter
    def full_name(self,new_name):
        if isinstance(new_name,str) and new_name.strip():
            self.__author_full_name = new_name.strip()
        else:
            raise ValueError       
                 
    @property
    def unique_id(self):
        return self.__unique_id

    def __repr__(self):
        return f"<Author {self.full_name}, author id = {self.unique_id}>"
    
    def __eq__(self,other):             #More or less Verified
        if not isinstance(other, self.__class__):
            return False
        return other.unique_id == self.unique_id
            
    def __lt__(self,other):               #More or less Verified
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id < other.unique_id

    def __hash__(self):                 #More or less Verified
        return hash(self.__unique_id)
    
    def add_coauthor(self,coauthor):   
        if type(coauthor) is Author:
            if coauthor.unique_id not in self.coauthors and coauthor.unique_id != self.__unique_id:
                self.coauthors.append(coauthor.unique_id)
                coauthor.add_coauthor(self)
        

    def check_if_this_author_coauthored_with(self,author):
        if type(author) is Author:
            return author.unique_id in self.coauthors

class Publisher:

    def __init__(self, publisher_name: str):
        self.__name = "N.A."
        self.name = publisher_name
        self.__publisher_id = hash(self.name)
        self.__books = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name):
        if isinstance(publisher_name,str) and publisher_name.strip():
            self.__name = publisher_name.strip()
            self.__publisher_id = hash(self.name)

    def __repr__(self):
        # we use access via the property here
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return self.__publisher_id

class Book:
    def __init__(self,book_id:int,book_title:str) -> None:
        self.__book_id = None
        self.__title = None
        self.__description = None
        self.__publisher = None
        # self.__publisher_name = None
        self.__authors = []
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = None
        self.__reviews = []
        self.__users = []

        if isinstance(book_id,int) and book_id >=0:
            self.__book_id = book_id
        else:
            raise ValueError
        self.title = book_title

    # @property
    # def publisher_name(self):
    #     return self.__publisher_name
    # @publisher_name.setter
    # def publisher_name(self,new_name):
    #     if new_name == "":
    #         self.__publisher_name = "N/A"
    #     else:
    #         self.__publisher_name = new_name

    def add_user(self,user):
        self.__users.append(user)
    @property
    def reviews(self):
        return self.__reviews
        
    def add_review(self,review):
        if isinstance(review,Review):
            if review not in self.__reviews:
                self.__reviews.append(review)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self,new_title):
        if isinstance(new_title,str) and new_title.strip():
            self.__title = new_title.strip()
        else:
            raise ValueError
    
    @property
    def book_id(self):
        return self.__book_id
    
    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self,new_description):
        if isinstance(new_description,str) and new_description.strip() != "":
            self.__description = new_description.strip()
    
    @property
    def publisher(self):
        return self.__publisher
    @publisher.setter
    def publisher(self,new_publisher):
        if isinstance(new_publisher,Publisher):
            self.__publisher = new_publisher
    
    @property
    def authors(self):
        return self.__authors
    
    @property
    def release_year(self):
        return self.__release_year
    @release_year.setter
    def release_year(self,new_year):
        if isinstance(new_year,int) and new_year >=0:
            self.__release_year = new_year
        else:
            raise ValueError
    
    @property
    def ebook(self):
        return self.__ebook
    @ebook.setter
    def ebook(self,new_bool):
        if isinstance(new_bool,bool):
            self.__ebook = new_bool
    
    @property
    def num_pages(self):
        return self.__num_pages
    @num_pages.setter
    def num_pages(self,new_num):
        if isinstance(new_num,int) and new_num >=0:
            self.__num_pages = new_num

    def __repr__(self) -> str:
        return f"<Book {self.title}, book id = {self.book_id}>"

    def __eq__(self, other) -> bool:
        if isinstance(other,Book):
            return self.book_id == other.book_id
        else:
            return False
    
    def __lt__(self,other):
        if isinstance(other,Book):
            return self.book_id < other.book_id
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.__book_id)
    

    def add_author(self,new_author):
        if isinstance(new_author,Author):
            if len(self.__authors) == 0:
                self.__authors.append(new_author)
            elif new_author not in self.__authors:
                for authors in self.__authors:
                    authors.add_coauthor(new_author)
                self.__authors.append(new_author)
    
    def remove_author(self,author):
        if isinstance(author,Author):
            if author in self.__authors:
                self.__authors.remove(author)

class BooksInventory:
    def __init__(self) -> None:
        self.__books_inventory = {}
        self.__book_title_dict = {}
        self.__all_books = []
    
    def add_book(self,book, price = 0, nr_books_in_stock = 0):
        if isinstance(book,Book) and type(price) in [int,float] and isinstance(nr_books_in_stock,int) and price >=0 or nr_books_in_stock >=0:
            storage_dict = {}
            storage_dict["book"] = book
            self.__book_title_dict[book.title] = book
            storage_dict["price"] = price
            storage_dict["nr_books_in_stock"] = nr_books_in_stock
            self.__books_inventory[book.book_id] = storage_dict
            insort_left(self.__all_books,book)
        else:
            raise ValueError   
    
    @property
    def all_books(self):
        return self.__all_books

    @property
    def books_inventory(self):
        return self.__books_inventory

    def __len__(self):
        return len(self.__all_books)

    def remove_book(self,book_id):
        if isinstance(book_id,int):
            if book_id in self.__books_inventory:
                self.__books_inventory.pop(book_id)

    def find_book(self,book_id): #BookID
        if isinstance(book_id,int):
           if book_id in self.__books_inventory:
               return self.__books_inventory[book_id]["book"]

    def find_price(self,book_id):
        if isinstance(book_id,int):
           if book_id in self.__books_inventory:
               return self.__books_inventory[book_id]["price"]
    
    def find_stock_count(self,book_id):
        if isinstance(book_id,int):
            if book_id in self.__books_inventory:
                return self.__books_inventory[book_id]["nr_books_in_stock"]
    
    def search_book_by_title(self,title):
        if isinstance(title,str):
            if title in self.__book_title_dict:
                return self.__book_title_dict[title]
    
    def get_random_books(self,n):
        return_list = []
        if isinstance(n,int):
            while len(return_list)!=n:
                temp = choice(self.__all_books)
                if len(return_list) == 0 or temp not in return_list:
                    return_list.append(temp)
            return return_list
        else:
            raise ValueError
            
class ReadingList:
    def __init__(self) -> None:
        self.reading_list = []
    
    def add_book(self,book):
        if isinstance(book,Book):
            if book not in self.reading_list:
                self.reading_list.append(book)
        
    def remove_book(self,book):
        if self.size() != 0:
            if isinstance(book,Book):
                self.reading_list.remove(book)
    
    def select_book_to_read(self,index):
        if index in range(0,self.size()):
            return self.reading_list[index]
        else:
            return None
    
    def size(self):
        return len(self.reading_list)
    
    def first_book_in_list(self):
        if self.size() == 0:
            return None
        else:
            return self.reading_list[0]

class Review:
    def __init__(self,book,review_text,rating,review_id = 0,user=None,timestamp = None) -> None:
        self.__book = None
        self.__review_text = 'N/A'
        self.__rating = None
        self.__id = None
        self.__user_associated = user
        if timestamp == None:
            self.__timestamp = datetime.datetime.now()
        else:
            self.__timestamp = timestamp
        
        if isinstance(book,Book):
            self.__book = book
        else:
            pass
            # raise ValueError
        if not isinstance(review_text,str) or review_text.strip()=="":
            pass
        else:
            self.__review_text = review_text.strip()
        if isinstance(rating,int) and rating in [1,2,3,4,5]:
            self.__rating = rating
        else:
            raise ValueError
    
    @property
    def user_associated(self):
        return self.__user_associated

    @property
    def user(self):
        return self.__user_associated

    @property
    def id(self):
        return self.__id
    @property
    def book(self):
        return self.__book
    
    @property
    def review_text(self):
        return self.__review_text
    
    @property
    def rating(self):
        return self.__rating
    
    @property
    def timestamp(self):
        return self.__timestamp
        
    def __repr__(self) -> str:
        # self.__id = None
        return f"Book {self.__book.title}, User: {self.__user_associated.user_name}, Rating: {self.__rating}, Review: {self.__review_text}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other,Review):
            return self.timestamp == other.timestamp and self.book == other.book and self.review_text == other.review_text and self.rating == other.rating
        else:
            return False

class User:
    def __init__(self,user_name:str,password:str,user_id:int=0) -> None:
        self.__user_name = None
        self.__password = None
        self.__read_books = []
        self.__reviews = []
        self.__pages_read = 0
        self.__reading_list = []
        self.__user_id = user_id
        if isinstance(user_name,str) and user_name.strip() != "":
            self.__user_name = user_name.strip().lower()
        if isinstance(password, str) and len(password) >=7:
            self.__password = password
    
    @property
    def user_id(self):
        return self.__user_id

    @property
    def reading_list(self):
        return self.__reading_list
    
    def add_book_to_reading_list(self,book:Book):
        # print('ran')
        if isinstance(book,Book):
            # if book.book_id not in self.__reading_list:
            
            if book not in self.__reading_list:
                if len(self.__reading_list)==10:
                    self.__reading_list.pop(0)    
                    # print("THIS RAN")
                
                self.__reading_list.append(book)
                # print(self.reading_list)
                # self.__reading_list.append(book.book_id)
            # scm.commit()
            
    
    def remove_book_from_reading_list(self,book:Book):
        if isinstance(book,Book):
            # if book.book_id in self.__reading_list:
            if book in self.__reading_list:
                self.__reading_list.remove(book)
                # self.__reading_list.remove(book.book_id)
        
    @property
    def user_name(self):
        return self.__user_name
    
    @property
    def password(self):
        return self.__password
    
    @property
    def read_books(self):
        return self.__read_books
    
    @property
    def reviews(self):
        return self.__reviews
    
    @property
    def pages_read(self):
        return self.__pages_read

    def __repr__(self) -> str:
        return f"<User {self.user_name}>"
    
    def __eq__(self, other) -> bool:
        if isinstance(other,User):
            return self.user_name == other.user_name
        else:
            return False
    
    def __lt__(self,other):
        if isinstance(other,User):
            return self.user_name < other.user_name
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self.user_name)
    
    def read_a_book(self,book):
        if isinstance(book,Book):
            if len(self.__read_books) == 0 or book not in self.__read_books:
                self.__read_books.append(book)
                self.__pages_read += book.num_pages
    
    def add_review(self,review):
        if isinstance(review,Review):
            if len(self.__reviews)== 0 or review not in self.__reviews:
                self.__reviews.append(review)

class ModelException(Exception):
    pass

def make_review(review_text:str,user:User,book:Book,rating:int):
    review = Review(book,review_text,rating,user=user)
    user.add_review(review)
    book.add_review(review)

    return review
