import abc
import re
from typing import List

from library.domain.model import User,Book,Review,Author,Publisher

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository():

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError
    
    def __len__(self):
        raise NotImplementedError

########################################        Users

    def add_user(self, user: User):
        raise NotImplementedError

    def get_user(self, user_name:str) -> User:
        raise NotImplementedError

########################################        Books

    def add_book(self, book: Book):
        raise NotImplementedError

    def get_book(self, id: int) -> Book:
        raise NotImplementedError

    def get_book_by_release_year(self, target_date: int) -> List[Book]:
        raise NotImplementedError

    def get_number_of_books(self) -> int:
        raise NotImplementedError

    def get_first_book(self):
        raise NotImplementedError

    def get_last_book(self):
        raise NotImplementedError
    
    def get_book_by_id(self,id:int):
        raise NotImplementedError

    def get_books_by_ids(self, id_list:List[int]):
        raise NotImplementedError

    def get_books_by_author_name(self,author_name: str):
        raise NotImplementedError

    def get_books_by_author_id(self,author_id: int):
        raise NotImplementedError

    def get_books_by_release_year(self,year:int):
        raise NotImplementedError

    def get_book_by_title_specific(self,title:str):
        raise NotImplementedError

    def get_book_by_title_general(self,title:str):
        raise NotImplementedError

    def get_books_by_publisher_name(self,publisher_name:str):
        raise NotImplementedError
    
    def get_all_books(self):
        raise NotImplementedError
    
########################################        Reviews

    def add_review(self, review: Review):
        pass #FOR DEBUGGING ONLY
        # if review.user is None or review not in review.user.reviews:
        #     raise RepositoryException('Review not correctly attached to a User')
        # if review.book is None or review not in review.book.reviews:
        #     raise RepositoryException('REview not correctly attached to an Article')

    def get_reviews(self):
        raise NotImplementedError

########################################        Recommendations

    def get_recommendations(self,user_name=None,no_of_books = 10):
        raise NotImplementedError
        
    def __find_recommendations(self,reading_list):
        raise NotImplementedError

########################################        Authors and Publishers
    
    def add_author(self,author:Author):
        raise NotImplementedError
    
    def get_author_names(self):
        raise NotImplementedError
    
    def get_author_ids(self):
        raise NotImplementedError
    
    def add_publisher(self,publisher:Publisher):
        raise NotImplementedError

    def get_all_publisher_names(self):
        raise NotImplementedError


########################################        Reading List

    def get_reading_list_for_user(self,user_name=None):
        raise NotImplementedError
    
    def add_book_to_reading_list(self,user:User,book:Book):
        raise NotImplementedError

