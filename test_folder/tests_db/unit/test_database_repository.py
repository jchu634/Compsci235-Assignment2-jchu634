from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Review, Author,Publisher,make_review
from library.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    user = User('Dave', '123456789',10)
    repo.add_user(user)
    repo.add_user(User('Martin', '123456789',9))
    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_book_count(session_factory_full_lite):
    repo = SqlAlchemyRepository(session_factory_full_lite)

    number_of_books = repo.get_number_of_books()

    # Check that the query returned 177 Books.
    assert number_of_books == 196

def test_repository_can_add_book(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    number_of_books = repo.get_number_of_books()

    new_book_id = number_of_books + 1

    book = Book(new_book_id,"HELLO WORLD"
    )
    repo.add_book(book)

    assert repo.get_book(new_book_id) == book

def test_repository_can_retrieve_book(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_book(12349665)

    # Check that the Book has the expected title.
    assert book.title == "Naoki Urasawa's 20th Century Boys, Volume 20 (20th Century Boys, #20)"

    # Check that the Book is reviewed as expected.
    review_one = [review for review in book.reviews if review.review_text == "I hope it's not as bad here as Italy!"][0]
    review_two = [review for review in book.reviews if review.review_text == 'Yeah Freddie, bad news'][0]

    assert review_one.user.user_name == 'fmercury'
    assert review_two.user.user_name == "derp"

    # Check that the Book is tagged as expected    
    assert book.authors == [Author(294649,'Naoki Urasawa')]
    assert book.publisher == Publisher('VIZ Media')

def test_repository_does_not_retrieve_a_non_existent_book(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_book(201)
    assert book is None

def test_repository_can_retrieve_author_names(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    author_names = repo.get_author_names()
    
    assert author_names[0] == 'Garth Ennis'
    assert author_names[5] == 'Andrea DiVito'
    assert author_names[-1] == 'Jason Delgado'

def test_repository_can_retrieve_author_ids(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    author_ids = repo.get_author_ids()
    
    assert author_ids[0] == 14965
    assert author_ids[5] == 79136
    assert author_ids[-1] == 16209952

def test_repository_can_retrieve_publisher_names(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    publisher_names = repo.get_all_publisher_names()
    
    assert publisher_names[0] == 'N.A.'
    assert publisher_names[5] == 'Avatar Press'
    assert publisher_names[-1] == 'Marvel'

def test_repository_can_get_first_book(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_first_book()
    assert book.title == 'Superman Archives, Vol. 2'

def test_repository_can_get_last_book(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_last_book()
    assert book.title == 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC'

def test_repository_can_get_books_by_ids(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_book_by_id(25742454)

    assert book.title == 'The Switchblade Mamma'

def test_repository_does_not_retrieve_book_for_non_existent_id(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_book_by_id(2)

    assert book == None

def test_repository_returns_book_for_author_name(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_author_name('DigiKore Studios')
    
    assert books == [repo.get_book_by_id(27036538)]

def test_repository_returns_books_for_author_name(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_author_name('Naoki Urasawa')
    
    assert len(books) == 3
    assert books[0] == repo.get_book_by_id(12349665)
    assert books[1] == repo.get_book_by_id(12349663)
    assert books[2] == repo.get_book_by_id(13340336)

def test_repository_returns_an_empty_list_for_non_existent_author_name(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_author_name('This does not exist')

    assert books == []

def test_repository_returns_book_for_author_id(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_books_by_author_id(5808419)
    
    assert book == [repo.get_book_by_id(27036538)]

def test_repository_returns_books_for_author_id(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_author_id(294649)
    
    assert len(books) == 3
    assert books[0] == repo.get_book_by_id(12349665)
    assert books[1] == repo.get_book_by_id(12349663)
    assert books[2] == repo.get_book_by_id(13340336)

def test_repository_returns_an_empty_list_for_non_existent_author_id(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_author_id(9137912)

    assert books == []

def test_repository_can_retrieve_books_by_release_year(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_release_year(2016)

    # Check that the query returned 3 Books.
    assert len(books) == 5

    # these books are no jokes...
    books = repo.get_books_by_release_year(2012)

    # Check that the query returned 5 Books.
    assert len(books) == 3

def test_repository_does_not_retrieve_an_book_when_there_are_no_books_for_a_given_release_year(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_release_year(1290)
    assert len(books) == 0

def test_repository_returns_book_for_title_specific(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_book_by_title_specific('Superman Archives, Vol. 2')
    
    assert books == [repo.get_book_by_id(707611)]

def test_repository_returns_book_for_title_general(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_book_by_title_general('Superman Archives, Vol.')
    
    assert books == [repo.get_book_by_id(707611)]

def test_repository_returns_books_for_title_general(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_book_by_title_general('20th Century Boys')
    
    assert len(books) == 3
    assert books[0] == repo.get_book_by_id(12349663)
    assert books[1] == repo.get_book_by_id(12349665)
    assert books[2] == repo.get_book_by_id(13340336)

def test_repository_returns_an_empty_list_for_non_existent_title(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_book_by_title_specific('This does not exist')
    assert books == []
    books = repo.get_book_by_title_general('This does not exist')
    assert books == []

def test_repository_returns_book_for_publisher_name(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_books_by_publisher_name('Planeta DeAgostini')
    
    assert book == [repo.get_book_by_id(13340336)]

def test_repository_returns_books_for_publisher_name(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_publisher_name('VIZ Media')
    
    assert len(books) == 2
    assert books[-1] == repo.get_book_by_id(12349665)
    assert books[0] == repo.get_book_by_id(12349663)

def test_repository_returns_an_empty_list_for_non_existent_author_id(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    books = repo.get_books_by_publisher_name("This does not exist")

    assert books == []

def test_repository_can_add_author(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    author = Author(99999,'This does not exist yet')
    repo.add_author(author)

    assert 'This does not exist yet' in repo.get_author_names()
    assert 99999 in repo.get_author_ids()

def test_repository_can_add_publisher(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    publisher = Publisher('This does not exist yet')
    repo.add_publisher(publisher)
    
    assert 'This does not exist yet' in repo.get_all_publisher_names()

def test_repository_can_add_a_review(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    user = repo.get_user('thorke')
    book = repo.get_book(13340336)
    review = make_review("Trump's onto it!", user, book,3)

    repo.add_review(review)

    assert review in repo.get_reviews()

def test_repository_does_not_add_a_review_without_a_user(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    book = repo.get_book(2)
    review = Review(book, "Trump's onto it!",5)

    with pytest.raises(RepositoryException):
        repo.add_review(review)

def test_repository_can_retrieve_reviews(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    assert len(repo.get_reviews()) == 4

def test_can_retrieve_an_book_and_add_a_review_to_it(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    # Fetch Book and User.
    book = repo.get_book(35452242)
    author = repo.get_user('thorke')

    # Create a new Review, connecting it to the Book and User.
    review = make_review('First death in Australia', author, book,5)

    book_fetched = repo.get_book(35452242)
    author_fetched = repo.get_user('thorke')


    assert review in book_fetched.reviews
    assert review in author_fetched.reviews

def test_can_add_book_to_reading_list(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    user = repo.get_user('thorke')
    for book_id in [707611, 2168737, 2250580, 11827783, 12349663, 12349665, 13340336, 13571772, 17405342, 18711343, 18955715, 23272155, 25742454, 27036536, 27036537, 27036538, 27036539, 30128855, 30735315, 35452242]:
        repo.add_book_to_reading_list(repo.get_book_by_id(book_id),user.user_name)
    
    assert user.reading_list == [repo.get_book_by_id(book_id) for book_id in [18955715, 23272155, 25742454, 27036536, 27036537, 27036538, 27036539, 30128855, 30735315, 35452242]]
    assert len(user.reading_list) == 10
    assert repo.get_book_by_id(707611) not in user.reading_list

def test_can_get_reccommendations_if_no_user(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    assert len(repo.get_recommendations())==10

def test_can_get_recommendations_if_fake_user(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    assert len(repo.get_recommendations('This is evidently fake')) == 10

def test_can_get_custom_amount_of_recommendations(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    assert len(repo.get_recommendations('This is evidently fake',no_of_books=15)) == 15
    #The repository will not validate if the number of books is valid
    # as this is designed to be a preset hardcoded value, with this being
    # an override

def test_can_get_recommendations_if_user_has_reading_list(session_factory_lite):
    repo = SqlAlchemyRepository(session_factory_lite)

    user = repo.get_user('thorke')
    for book_id in [707611, 2168737, 2250580, 11827783, 12349663, 12349665, 13340336, 13571772, 17405342, 18711343, 18955715, 23272155, 25742454, 27036536, 27036537, 27036538, 27036539, 30128855, 30735315, 35452242]:
        repo.add_book_to_reading_list(repo.get_book_by_id(book_id),user.user_name)

    assert repo.get_book_by_id(17405342) in repo.get_recommendations(user.user_name)


