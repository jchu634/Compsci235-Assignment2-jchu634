import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import ReadingList, User, Book, Review,Author, Publisher,make_review

book_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Andrew".lower()
    new_password = "12345678"

    if values is not None:
        new_name = values[0].lower()
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_user_name(empty_session, values=None):
    new_name = "Andrew".lower()
    new_password = "12345678"

    if values is not None:
        new_name = values[0].lower()
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_name from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values=None):
    if values == None:
        values = [['derp','adjigasufvaf',3],['GenericUser123','thinkingishard',5]]
    for value in values:
        empty_session.execute('INSERT INTO users (id,user_name, password) VALUES (:id, :user_name, :password)',
                              {'id':value[2],'user_name': value[0].lower(), 'password': value[1]})
    rows = list(empty_session.execute('SELECT * from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (id,release_year,title, description) VALUES'
        '(111,2017, "Coronavirus: First case of virus in New Zealand", '
        '"The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.")'
    )
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]

def insert_publishers(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (name,id) VALUES ("Generic Publisher",567), ("UnGeneric Publisher",729)'
    )
    rows = list(empty_session.execute('SELECT id from publishers'))
    keys = tuple(row[0] for row in rows)
    
    return keys

def insert_publishers_name(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (name,id) VALUES ("Generic Publisher",567), ("UnGeneric Publisher",729)'
    )
    rows = list(empty_session.execute('SELECT name from publishers'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_authors(empty_session):
    empty_session.execute(
        'INSERT INTO authors (id,name) VALUES (981,"Frank Frankenstein"),(675,"Jack Jackenstein")'
    )
    rows = list(empty_session.execute('SELECT id from authors'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book_author_associations(empty_session, book_key, author_keys):
    stmt = 'INSERT INTO books_authors (book_id, author_id) VALUES (:book_id, :author_id)'
    for author_key in author_keys:
        empty_session.execute(stmt, {'book_id': book_key, 'author_id': author_key})

def insert_book_user_associations(empty_session, book_key, user_keys):
    stmt = 'INSERT INTO user_reading_list (book_id, user_id) VALUES (:book_id, :user_id)'
    for user_key in user_keys:
        empty_session.execute(stmt, {'book_id': book_key, 'user_id': user_key})

def insert_reviewed_book(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user_name(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (id, user_name, book_id, review_text, timestamp,rating) VALUES '
        '(1,:user_name, :book_id, "Review 1", :timestamp_1,5),'
        '(2,:user_name, :book_id, "Review 2", :timestamp_2,4)',
        {'user_name': user_key, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]

def make_book(empty_session):
    book = Book(111,"Coronavirus: First case of virus in New Zealand"
    )
    book.description = 'TEST TEST TEST'
    book.publisher = Publisher(insert_publishers_name(empty_session)[0])
    book.release_year = 1997
    return book

def make_user():
    user = User("Andrew", "1234567")
    return user

def make_author():
    author = Author(3,"Humpty Dumpty")
    return author

def make_publisher():
    publisher = Publisher("News")
    return publisher

def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234",3))
    users.append(("Cindy", "1111",5))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "1234567")]

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234567"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "1234567")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book(empty_session)
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id

def test_loading_of_author_book(empty_session):
    book_key = insert_book(empty_session)
    author_keys = insert_authors(empty_session)
    insert_book_author_associations(empty_session, book_key, author_keys)

    book = empty_session.query(Book).get(book_key)
    authors = [empty_session.query(Author).get(key) for key in author_keys]

    for author in authors:
        assert author in book.authors
        assert book in author._Author__books

def test_loading_of_reading_list(empty_session):
    book_key = insert_book(empty_session)
    user_keys = insert_users(empty_session)
    
    insert_book_user_associations(empty_session, book_key, user_keys)

    book = empty_session.query(Book).get(book_key)
    users = [i for i in empty_session.query(User).all() if i.user_id in user_keys]
    
    for user in users:
        assert book in user._User__reading_list
        assert user in book._Book__users

def test_loading_of_reviewed_book(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book

def test_saving_of_review(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user_name(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "andrew").one()

    # Create a new Review that is bidirectionally linked with the User and Book.
    review_text = "Some review text."
    review = make_review(review_text, user, book,5)

    # Note: if the bidirectional links between the new Review and the User and
    # Book objects hadn't been established in memory, they would exist following
    # committing the addition of the Review to the database.
    empty_session.add(review)
    empty_session.commit()
    
    rows = list(empty_session.execute('SELECT user_name, book_id, review_text FROM reviews'))

    assert rows == [(user_key, book_key, review_text)]

def test_saving_of_book(empty_session):
    book = make_book(empty_session)
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, release_year, title, description, publisher_name FROM books'))
    
    assert rows == [(111, 1997, 'Coronavirus: First case of virus in New Zealand', 'TEST TEST TEST', None)]

def test_saving_authored_book(empty_session):
    book = make_book(empty_session)
    author = make_author()
    book.add_author(author)

    # Persist the Book (and Author).
    # Note: it doesn't matter whether we add the Author or the Book. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_book() checks for insertion into the books table.
    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT id, name FROM authors'))
    author_key = rows[0][0]
    assert rows[0][1] == "Humpty Dumpty"

    # Check that the book_authors table has a new record.
    rows = list(empty_session.execute('SELECT book_id, author_id from books_authors'))
    book_foreign_key = rows[0][0]
    author_foreign_key = rows[0][1]

    assert book_key == book_foreign_key
    assert author_key == author_foreign_key

def test_saving_reading_list(empty_session):
    book = make_book(empty_session)
    user = make_user()

    # Establish the bidirectional relationship between the Book and the Tag.
    user.add_book_to_reading_list(book)

    # Persist the Book (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Book. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_book() checks for insertion into the books table.
    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT id, user_name FROM users'))
    user_key = rows[0][0]
    assert rows[0][1] == "andrew"

    # Check that the book_tags table has a new record.
    rows = list(empty_session.execute('SELECT book_id, user_id from user_reading_list'))
    book_foreign_key = rows[0][0]
    user_foreign_key = rows[0][1]

    assert book_key == book_foreign_key
    assert user_key == user_foreign_key

def test_save_reviewed_book(empty_session):
    # Create Book User objects.
    book = make_book(empty_session)
    user = make_user()

    # Create a new Review that is bidirectionally linked with the User and Book.
    review_text = "Some review text."
    review = make_review(review_text, user, book,5)

    # Save the new Book.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_book() checks for insertion into the books table.
    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT user_name FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that links to the books and users
    # tables.
    rows = list(empty_session.execute('SELECT user_name, book_id, review_text FROM reviews'))
    assert rows == [(user_key, book_key, review_text)]

