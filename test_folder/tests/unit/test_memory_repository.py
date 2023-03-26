from datetime import date, datetime
from typing import List
from attr.validators import in_

import pytest
from library.adapters import memory_repository

from library.domain.model import User, Book,Publisher,Author,Review
# from library.adapters.repository import RepositoryException

def test_repository_can_add_book(in_memory_repo):
    book = Book(1111,"THIS IS A TEST")
    authors = [Author(1,"Hello World"),Author(2,"HPO OPH")]
    book.add_author(authors[0])
    book.add_author(authors[1])
    book.publisher = Publisher("TESTTEST")
    in_memory_repo.add_book(book)
    

    assert in_memory_repo.get_book(1111) is book
    assert "Hello World" in in_memory_repo.get_author_names()
    assert "HPO OPH" in in_memory_repo.get_author_names()
    assert 1 in in_memory_repo.get_author_ids()
    assert 2 in in_memory_repo.get_author_ids()
    assert "TESTTEST" in in_memory_repo.get_all_publisher_names()
    book1 = Book(1111,"THIS IS A TEST")
    book1.publisher = Publisher("TESTTESTTEST")
    in_memory_repo.add_book(book1)
    assert "TESTTESTTEST" in in_memory_repo.get_all_publisher_names()
    

def test_repository_can_get_book(in_memory_repo):
    book = in_memory_repo.get_book(12349663)
    assert book == Book(12349663,"Naoki Urasawa's 20th Century Boys, Volume 19 (20th Century Boys, #19)")

def test_repository_DNGNEB(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    #Because its difficult to test name on Window's console
    book = in_memory_repo.get_book(1)
    assert book is None

def test_repository_can_get_no_of_books(in_memory_repo):
    count = in_memory_repo.get_number_of_books()
    assert count == 20

def test_repository_can_get_book_by_author_name(in_memory_repo):
    book = in_memory_repo.get_books_by_author_name("Yuu Asami")
    assert len(book) == 1
    assert book[0].book_id == 2250580
    assert book[0].title == "A.I. Revolution, Vol. 1"

    books = in_memory_repo.get_books_by_author_name("Naoki Urasawa")
    assert len(books) == 3
    assert books[0].book_id == 12349663
    assert books[1].book_id == 12349665
    assert books[2].book_id == 13340336
    assert books[0].title == "Naoki Urasawa's 20th Century Boys, Volume 19 (20th Century Boys, #19)"
    assert books[1].title == "Naoki Urasawa's 20th Century Boys, Volume 20 (20th Century Boys, #20)"
    assert books[2].title == "20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)"
    

def test_repository_DNGNEB_by_author_name(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    books = in_memory_repo.get_books_by_author_name("Cthulu All-spark")
    assert len(books) ==0

def test_repository_can_get_books_by_author_id(in_memory_repo):
    book = in_memory_repo.get_books_by_author_id(1015982)
    assert len(book) == 1
    assert book[0].book_id == 2250580
    assert book[0].title == "A.I. Revolution, Vol. 1"
    
    books = in_memory_repo.get_books_by_author_id(294649)
    assert len(books) == 3
    assert books[0].book_id == 12349663
    assert books[1].book_id == 12349665
    assert books[2].book_id == 13340336
    assert books[0].title == "Naoki Urasawa's 20th Century Boys, Volume 19 (20th Century Boys, #19)"
    assert books[1].title == "Naoki Urasawa's 20th Century Boys, Volume 20 (20th Century Boys, #20)"
    assert books[2].title == "20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)"
    

def test_repository_DNGNEB_by_author_id(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    books = in_memory_repo.get_books_by_author_id(60221515)
    assert len(books) == 0

def test_repository_can_get_book_by_release_year(in_memory_repo):
    book = in_memory_repo.get_books_by_release_year(1997)
    assert len(book) == 1
    assert book[0].book_id == 707611
    assert book[0].title == "Superman Archives, Vol. 2"

    books = in_memory_repo.get_books_by_release_year(2016)
    assert len(books) == 5
    assert books[0].book_id == 27036536
    assert books[1].book_id == 27036537
    assert books[2].book_id == 27036538
    assert books[0].title == "War Stories, Volume 3"
    assert books[1].title == "Crossed, Volume 15"
    assert books[2].title == "Crossed + One Hundred, Volume 2 (Crossed +100 #2)"

def test_repository_DNGNEB_by_release_year(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    book = in_memory_repo.get_books_by_release_year(314159)
    assert len(book) == 0

def test_repository_can_get_book_by_title(in_memory_repo):
    book = in_memory_repo.get_book_by_title_specific("War Stories, Volume 3")
    assert len(book) == 1
    assert book[0].book_id == 27036536

    another_book = in_memory_repo.get_book_by_title_general("SuperMan")
    assert len(another_book) == 1
    assert another_book[0].book_id == 707611

def test_repository_DNGNEB_(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    book = in_memory_repo.get_book_by_title_specific("The Adventures of Cthulu All-Spark")
    book_again = in_memory_repo.get_book_by_title_general("The Adventures of Cthulu All-Spark")
    assert len(book) == 0
    assert len(book_again) == 0

def test_repository_can_get_book_by_publisher_name(in_memory_repo):
    book = in_memory_repo.get_books_by_publisher_name("Dynamite Entertainment")
    assert len(book) == 1
    assert book[0].book_id == 11827783
    
    books = in_memory_repo.get_books_by_publisher_name("VIZ Media")
    assert len(books) == 2
    assert books[0].book_id == 12349663
    assert books[1].book_id == 12349665

def test_repository_DNGNEB_(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    book = in_memory_repo.get_books_by_publisher_name("Kash and the Register")
    assert len(book) == 0

def test_get_recommendations_with_no_user(in_memory_repo):
    books = in_memory_repo.get_recommendations()
    assert len(books) == 10
    books = in_memory_repo.get_recommendations(None,5)
    assert len(books) == 5


def test_repository_(in_memory_repo):
    pass #These are incomplete for copy paste

def test_repository_DNGNEB_(in_memory_repo):
    #DNGNEB: Does_not_get_non_existant_book
    pass #These are incomplete for copy paste