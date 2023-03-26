from sqlalchemy import select, inspect

from library.adapters.orm import metadata
import datetime

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    # print(inspector.get_table_names())
    assert inspector.get_table_names() == ['authors', 'books', 'books_authors', 'publishers', 'reviews', 'user_reading_list', 'users']

def test_database_populate_select_all_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append((row['id'],row['name']))
        # print(all_authors)
        assert all_authors == [(14965, 'Garth Ennis'),(24594, 'Mike Wolfer'), (24781, 'Dan Slott'), (37450, 'Ed Brubaker'), (61231, 'Scott Beatty'), 
                                (79136, 'Andrea DiVito'), (81563, 'Jerry Siegel'), (89537, 'Joe Shuster'), (93069, 'Rich Tommaso'), (131836, 'Keith Burns'), 
                                (169661, 'Kieron Dwyer'), (294649, 'Naoki Urasawa'), (311098, 'Katsura Hoshino'), (791996, 'Maki Minami'), (853385, 'Chris  Martin'), 
                                (1015982, 'Yuu Asami'), (1251983, 'Rafael Ortiz'), (3188368, 'Tomas Aira'), (3274315, 'Florence Dupre la Tour'), (4346284, 'Jaymes Reed'), 
                                (4391289, 'Jeon Geuk-Jin'), (4980321, 'Daniel Indro'), (5808419, 'DigiKore Studios'), (6384773, 'Asma'), (6869276, 'Takashi   Murakami'), 
                                (7359735, 'Cun Shang Chong'), (7507599, 'Matt Martin'), (8224446, 'Fernando Heinz'), (8551671, 'Lindsey Schussman'), (14155472, 'Simon Spurrier'), (16209952, 'Jason Delgado')]

def test_database_populate_select_all_books(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['id'], row['title'],row['release_year'],row['description'],row['publisher_name']))

        nr_books = len(all_books)
        
        assert nr_books == 20
        assert all_books[0] == (707611, 'Superman Archives, Vol. 2', 1997, "These are the stories that catapulted Superman into the spotlight as one of the world's premier heroes of fiction. These volumes feature his earliest adventures, when the full extent of his powers was still developing and his foes were often bank robbers and crooked politicians.", 'DC Comics')

def test_database_populate_select_books_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_authors_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_books_authors_table]])
        result = connection.execute(select_statement)

        all_books_authors = []
        for row in result:
            all_books_authors.append((row['book_id'], row['author_id']))

        nr_books_authors = len(all_books_authors)
        
        assert nr_books_authors == 35
        assert all_books_authors[0] == (25742454, 8551671)
        assert all_books_authors[34] == (18955715, 311098)

def test_database_populate_select_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_authors_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_books_authors_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append((row['id'], row['name']))
        
        assert all_publishers[0][1] == 'N.A.'
        assert all_publishers[10][1] == 'Marvel'

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            # print(row)
            all_reviews.append((row['id'], row['user_name'], row['book_id'], row['review_text'],row['rating'],row['timestamp']))
        # print(all_reviews)
        assert all_reviews == [(1, 'derp', 12349663, 'Oh no, COVID-19 has hit New Zealand', 4, datetime.datetime(2020, 2, 28, 14, 31, 26)), 
                                (2, 'derp', 12349665, 'Yeah Freddie, bad news', 5, datetime.datetime(2020, 2, 28, 14, 39, 51)), 
                                (3, 'fmercury', 12349665, "I hope it's not as bad here as Italy!", 3, datetime.datetime(2020, 2, 29, 8, 12, 8)), 
                                (4, 'fmercury', 707611, 'Doop,TestTestTestTestTestTest"', 2, datetime.datetime(2018, 12, 19, 6, 47, 57))]

def test_database_populate_select_user_reading_lists(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_user_reading_lists_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_user_reading_lists_table]])
        result = connection.execute(select_statement)

        all_user_reading_lists = []
        for row in result:
            all_user_reading_lists.append((row['book_id'], row['user_id']))

        assert all_user_reading_lists == [(11827783, 5)]

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])
        assert all_users == ['thorke', 'fmercury', 'mjackson', 'test', 'derp']




