from datetime import date
from typing import List
from unicodedata import name

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from random import sample

from sqlalchemy.sql import base
from sqlalchemy.sql.schema import Table
from library.domain.model import User, Book, Review, Author,Publisher
from library.adapters.repository import AbstractRepository, RepositoryException

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

########################################        Users

    def add_user(self, user: User):
        if self._session_cm.session.query(User).filter(User._User__user_id == user.user_id).first() == None:
            with self._session_cm as scm:
                scm.session.add(user)
                scm.commit()
        else:
            if self._session_cm.session.query(User).filter(User._User__user_name == user.user_name).first() == None:
                check = self._session_cm.session.query(User).order_by(desc(User._User__user_id)).first()
                temp = User(user_name=user.user_name,password=user.password,user_id=check.user_id + 1)
                for book in user.reading_list:
                    user.add_book_to_reading_list(book)

                with self._session_cm as scm:
                    scm.session.add(temp)
                    scm.commit()

            

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name.lower()).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

########################################        Books

    def add_book(self, book: Book):
        with self._session_cm as scm:
            # print(book.authors)
            self.add_publisher(book.publisher)
            # for authors in book.authors:
            #     self.add_author(authors)
            
            scm.session.add(book)
            scm.commit()
            
    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == id).one()

        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return book
    
    def get_number_of_books(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def get_first_book(self):
        book = self._session_cm.session.query(Book).first()
        return book

    def get_last_book(self):
        book = self._session_cm.session.query(Book).order_by(desc(Book._Book__book_id)).first()
        return book

    def get_book_by_id(self,id:int): #This is just for clarity's sake on the search side
        return self.get_book(id)

    #UNUSED METHOD
    # def get_books_by_id(self, id_list: List[int]): 
    #     books = self._session_cm.session.query(Book).filter(Book._book__id.in_(id_list)).all()
    #     return books

    def get_books_by_author_name(self,author_name: str):
        if not isinstance(author_name,str) or author_name == "":
            return []
        row = self._session_cm.session.execute('SELECT id FROM authors WHERE authors.name = :author_name',{'author_name':author_name}).fetchone()
        if row is None:
            return []
        else:
            author_id = int(row[0])
            row = self._session_cm.session.execute('SELECT books.id from books INNER JOIN books_authors WHERE books_authors.author_id = :author_id AND books_authors.book_id = books.id',{'author_id':author_id}).fetchall()
            if row is None:
                return []
            else:
                return_books = []
                for i in range(len(row)):
                    return_books.append(self._session_cm.session.query(Book).filter(Book._Book__book_id == int(row[i][0])).one())
                return return_books

    def get_books_by_author_id(self,author_id:int):
        if not isinstance(author_id,int) or author_id < 0:
            return []
        row = self._session_cm.session.execute('SELECT books.id from books INNER JOIN books_authors WHERE books_authors.author_id = :author_id AND books_authors.book_id = books.id',{'author_id':author_id}).fetchall()
        if row is None:
            return []
        else:
            return_books = []
            for i in range(len(row)):
                return_books.append(self._session_cm.session.query(Book).filter(Book._Book__book_id == int(row[i][0])).one())
            return return_books

    def get_books_by_release_year(self, target_date: int) -> List[Book]:
        if target_date is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching target_date; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book._Book__release_year == target_date).all()
            #BANDAID FIX REMEMBER TO FIX ME
            # books = [book for book in self._session_cm.session.query(Book).all() if book.release_year == target_date]
            
            return books

    def get_book_by_title_specific(self,title:str):
        if title is None:
            return []
        else:
            books = self._session_cm.session.query(Book).filter(Book._Book__title == title).all()
            return books

    def get_book_by_title_general(self,title:str):
        if title is None:
            return []
        else:
            
            
            books = self._session_cm.session.query(Book).filter(Book._Book__title.contains(title)).all()
            #BANDAID FIX REMEMBER TO FIX ME
            # books = [book for book in self._session_cm.session.query(Book).all() if title.lower() in book.title.lower()]
            
            return books

    def get_books_by_publisher_name(self,publisher_name:str):
        if publisher_name is None:
            return []
        else:
            # Return books matching publisher_name; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book.publisher_name == publisher_name).all()
            #BANDAID FIX REMEMBER TO FIX ME
            # books = [book for book in self._session_cm.session.query(Book).all() if book.release_year == publisher_name]
            
            return books

    def get_all_books(self):
        books = self._session_cm.session.query(Book).all()
        return books
    
########################################        Reviews

    def add_review(self, review: Review):
        if review.user_associated == None:
            raise RepositoryException
        with self._session_cm as scm:          
            scm.session.add(review)
            scm.commit()
    
    def add_review_raw(self, book,review_text,rating,user_id):
        with self._session_cm as scm:
            scm.session.add(Review(book,review_text,rating,user_id))
            scm.commit()

    def get_reviews(self):
        return self._session_cm.session.query(Review).all()

########################################        Authors and Publishers

    def add_author(self,author:Author): # UNTESTED
        if isinstance(author,Author):
            # print(self._session_cm.session.query(Author).filter(Author._Author__unique_id == author.unique_id).first())
            if self._session_cm.session.query(Author).filter(Author._Author__unique_id == author.unique_id).first() == None:
                with self._session_cm as scm:
                    scm.session.add(author)
                    scm.commit()

    def get_author_names(self):
        Authors = []
        try:
            Authors = [Author.full_name for Author in self._session_cm.session.query(Author).all()]
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return Authors

    def get_author_ids(self):
        Authors = []
        try:
            Authors = [Author.unique_id for Author in self._session_cm.session.query(Author).all()]
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return Authors

    def add_publisher(self,publisher:Publisher):
        if isinstance(publisher,Publisher):
            
            # print(self._session_cm.session.query(Publisher).filter(Publisher.name==publisher.name).first())
            if self._session_cm.session.query(Publisher).filter(Publisher._Publisher__name==publisher.name).first() == None:
                with self._session_cm as scm:

                        scm.session.add(publisher)
                        scm.commit()

    def get_all_publisher_names(self):
        Publishers = []
        try:
            Publishers = [Publisher.name for Publisher in self._session_cm.session.query(Publisher).all()]
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return Publishers

########################################        Recommendations

    def add_book_to_reading_list(self,book:Book,user_name:str):
        user = self.get_user(user_name)
        
        
        user.add_book_to_reading_list(book)
        book.add_user(user)
        

        # self._session_cm.session.execute('INSERT INTO user_reading_list (book_id,user_id) VALUES (:book_id,:user_id)',{':book_id':book.book_id,':user_id':user.user_id})

        self._session_cm.commit()
        # with self._session_cm as scm:
        #     if scm.session.execute('SELECT books.id from user_reading_list a WHERE a.user_id = :user_id: AND book)
        #     scm.session.execute('SELECT books.id from books INNER JOIN books_authors WHERE books_authors.author_id = :author_id AND books_authors.book_id = books.id',{'author_id':author_id}).fetchall()
        
    def get_random_books(self,no_of_books:int):
        return sample(self.get_all_books(),no_of_books)

    def get_recommendations(self,user_name=None,no_of_books:int = 10):
        # print(self.get_random_books(no_of_books))
        
        if isinstance(user_name,str):
            user = self.get_user(user_name)
            if user == None:
                return self.get_random_books(no_of_books)
            else:
                
                if len(user.reading_list) > 0:
                    recommendations = self.__find_recommendations(user.reading_list)
                    # print(recommendations)
                    if len(recommendations) < no_of_books:
                        return recommendations + self.get_random_books(no_of_books-len(recommendations))
                    elif len(recommendations)>= no_of_books:
                        return recommendations[0:10]
            
        return self.get_random_books(no_of_books)
        
    def __find_recommendations(self,reading_list):
        return_list = {}
        for books in reading_list:
            for authors in books.authors:
                for book in self.get_books_by_author_id(authors.unique_id):
                    if book not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=4
                        else:
                            return_list[book.book_id] = [book,1]
            
            if books.release_year != None:
                for book in self.get_books_by_release_year(books.release_year):
                    if book not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=1
                        else:
                            return_list[book.book_id] = [book,1]
                for book in self.get_books_by_release_year(books.release_year-1):
                    if book not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=1
                        else:
                            return_list[book.book_id] = [book,1]
                for book in self.get_books_by_release_year(books.release_year+1):
                    if book not in reading_list:
                        if book.book_id in return_list:
                            return_list[book.book_id][1]+=1
                        else:
                            return_list[book.book_id] = [book,1]
            # print(book)
            # print(book.publisher)
            for book in self.get_books_by_publisher_name(books.publisher.name):
                if book not in reading_list:
                    if book.book_id in return_list:
                        return_list[book.book_id][1]+=2
                    else:
                        return_list[book.book_id] = [book,1]
        return [self.get_book_by_id(item[0]) for item in sorted(return_list.items(),key=lambda x: x[1][1])]