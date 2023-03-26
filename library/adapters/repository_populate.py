#from pathlib import Path

import csv
from tqdm import tqdm
from datetime import datetime
from werkzeug.security import generate_password_hash

import ast
from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Author, Book,Publisher,BooksInventory, ReadingList, User, Review, BooksInventory

def read_json_file(books_file_name:str,authors_file_name:str):
    json_reader = BooksJSONReader(books_file_name,authors_file_name)
    json_reader.read_json_files()

    return json_reader.dataset_of_books,json_reader.authors

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
    

def load_books(data_path: str, repo: AbstractRepository):
    print("Loading Books")
    temp = read_json_file(books_file_name=data_path+"\\data\\books.json",authors_file_name=data_path+"\\data\\authors.json")
    for author in tqdm(temp[1]):
        repo.add_author(author)
    for books in tqdm(temp[0]):
        repo.add_book(books)
    


def load_users(data_path: str, repo: AbstractRepository):
    users = []
    print("Loading Users")
    users_filename = data_path + "\\data\\users.csv"
    
    for data_row in tqdm(read_csv_file(users_filename)):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2]),
            user_id=int(data_row[0])
        )
        
        temp = ast.literal_eval(data_row[3])
        if len(temp) != 0:
            for book_id in temp:
                user.add_book_to_reading_list(repo.get_book_by_id(book_id))
        repo.add_user(user)
        users.append(user)
    return users

def load_reviews(data_path: str, repo: AbstractRepository, users):
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

def populate(repo: AbstractRepository,data_path:str="library\\adapters", database_mode: bool=False,lite=False):
    
    # Load articles and tags into the repository.
    load_books(data_path, repo)
    if not lite:
        # Load users into the repository.
        users = load_users(data_path, repo)

        # Load Reviews into the repository.
        load_reviews(data_path, repo, users)
    
