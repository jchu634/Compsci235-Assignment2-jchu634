from werkzeug.wrappers import response
# import requests
import pytest
from flask import session




def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'

def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Search for Books' in response.data
    assert b'List all Books' in response.data

def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/review?book_id=707611')
    response = client.post(
        '/review?book_id=707611',
        data={'review': 'Who needs quarantine query?', 'book_id': 707611,'rating':3}    )
    assert response.status_code == 200
    # assert response.headers['Location'] == 'http://localhost/search/4/query?book_id=707611' #Changed Behaviour in Assignment 3

@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks Trump is a f***wit/query?', (b'Your review must not contain profanity')),
        ('Hey', (b'Your review is too short')),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review on an book.
    response = client.post(
        '/review',
        data={'review': review, 'book_id': 707611,'rating':1},
        follow_redirects=True
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert response.status_code == 200
        assert message in response.data

#########################################################################################################################################################
# TESTS FOR LIST
#########################################################################################################################################################

def test_list_index(client):
    response = client.get('/list')
    assert response.status_code == 200
    assert b'Next Page' in response.data
    assert b'Press Table Headers to sort table.' in response.data
    assert b'707611' in response.data
    assert b'2168737' in response.data

def test_list_pages(client):
    response = client.get('/list?page=2')
    
    assert response.status_code == 200
    
    assert b'Previous Page' in response.data
    assert b'Press Table Headers to sort table.' in response.data
    assert b'18955715' in response.data
    assert b'23272155' in response.data
    
#########################################################################################################################################################

def test_list_pages_invalid_page(client):
    response = client.get('/list?page=9999999')
    response_1 = client.get('/list?page=-128743614671215')
    response_2 = client.get('/list?page=')

    assert response.status_code == 200
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    
    assert b'Previous Page' in response.data
    assert b'Press Table Headers to sort table.' in response.data
    assert b'18955715' in response.data
    assert b'23272155' in response.data

    assert b'Next Page' in response_1.data
    assert b'Press Table Headers to sort table.' in response_1.data
    assert b'707611' in response_1.data
    assert b'2168737' in response_1.data

    assert b'Next Page' in response_2.data
    assert b'Press Table Headers to sort table.' in response_2.data
    assert b'707611' in response_2.data
    assert b'2168737' in response_2.data

def test_search_list_pages(client):
    response = client.get('/search/1/query?release_year=2012')

    assert response.status_code == 200
    assert b'Press Table Headers to sort table.' in response.data


#########################################################################################################################################################
#   TESTS FOR SEARCH FORMS        
#   (NOTE: These will test only a few inputs as the search is handled by search queries, which are more thoroughly tested with the exception for author   
#   as it handles things different due to two optional arguments and general search as it has a bit more specialised handling in a different form)
#   Default Behaviour (INT) is RightType = 302 Redirect, WrongType/NoInput = 200 Return the form with additional Information
#   Default Behaviour (STR) is RightType/NoInput/WrongType = 302 Redirect
#########################################################################################################################################################

def test_search_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search')
    assert response.status_code == 308 #Redirect
    response_1 = client.get('/search/')
    assert response_1.status_code == 200 #Redirect

    #Checking that Elements are appearing
    #Not checking in response for /search as that is a redirect
    assert b'Search By Author' in response_1.data
    assert b'Search By Release Year' in response_1.data
    assert b'Search By Title' in response_1.data
    assert b'Search By Publisher' in response_1.data
    assert b'Search By ID' in response_1.data
    assert b'General Search' in response_1.data

def test_search_author_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search/0')
    assert response.status_code == 200 #Redirect

    #Checking that Elements are appearing
    assert b'Fill in at least 1 field' in response.data
    assert b'Author Name' in response.data
    assert b'Author ID:' in response.data
    assert b'Find' in response.data

@pytest.mark.parametrize(('author_name','author_id','messages'), (
        ('Katsura Hoshino',311098, 1),
        ('Jeon Geuk-Jin',4391289, 1),
        ('Lindsey Schussman',8551671, 1),
))
def test_search_author_index_with_correct_input(client,author_name,author_id,messages):
    # Attempt to search with author name only
    response = client.post(
        '/search/0',
        data={
            'name': author_name
            }
    )
    # Check that supplying correct Author IDs returns a result i.e. 302 Redirect.
    for i in range(messages):
        assert response.status_code == 302
    
    #Attempt to search with author id only
    response = client.post(
        '/search/0',
        data={
            'id': author_id
            }
    )
    # Check that supplying correct Author Names returns a result i.e. 302 Redirect.
    for i in range(messages):
        assert response.status_code == 302
    
    #Attempt to search with author id and author_name
    response = client.post(
        '/search/0',
        data={
            'id': author_id,
            'name': author_name
            }
    )
    # Check that supplying correct Author IDs returns a result i.e. 302 Redirect.
    for i in range(messages):
        assert response.status_code == 302

def test_search_author_index_with_incorrect_inputs(client):
    # Attempt to search with wrong author name only (Right Type)
    response = client.post(
        '/search/0',
        data={
            'name': "Hello"
            }
    )
    #Attempt to search with wrong author id only (Right Type)
    response_1 = client.post(
        '/search/0',
        data={
            'id': 1
            }
    )
    #Attempt to search with wrong author id and wrong authorname (Right Type)
    response_2 = client.post(
        '/search/0',
        data={
            'id': 1,
            'name': "Hello"
            }
    )
    # Check that supplying incorrect data with the right type returns a redirect (302) to be handled elsewhere
    assert response.status_code == 302
    assert response_1.status_code == 302
    assert response_2.status_code == 302
        
    # Attempt to search with wrong author name only (Wrong Type)
    response = client.post(
        '/search/0',
        data={
            'name': 1
            }
    )
    #Check that supplying author name with the wrong type redirects
    assert response.status_code == 302
    #Attempt to search with wrong author id only (Wrong Type)
    response_1 = client.post(
        '/search/0',
        data={
            'id': "Hello"
            }
    )
    #Attempt to search with wrong author id and wrong authorname (Wrong Type)
    response_2 = client.post(
        '/search/0',
        data={
            'id': "Hello",
            'name': 0
            }
    )
    # Check that supplying data with the wrong type returns the form with additional information
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert b"Invalid Input/s" in response_1.data
    assert b"Invalid Input/s" in response_2.data

    # Attempt to search with None as data
    response = client.post(
        '/search/0',
        data={
            'id': None
            }
    )
    response_1 = client.post(
        '/search/0',
        data={
            'name': None
            }
    )
    response_2 = client.post(
        '/search/0'
    )
    # Check that supplying no data redirects (This is because of the nature of having two different inputs)
    assert response.status_code == 302
    assert response_1.status_code == 302
    assert response_2.status_code == 302

################################################################################################################

def test_search_release_year_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search/1')
    assert response.status_code == 200 #Redirect

    #Checking that Elements are appearing
    assert b'Release Year:' in response.data
    assert b'Find' in response.data
    
def test_search_release_year_with_correct_input(client):
    # Attempt to search with release year
    response = client.post(
        '/search/1',
        data={
            'id': 1997
            }
    )
    # Check that supplying correct data returns a result i.e. 302 Redirect.
    assert response.status_code == 302

def test_search_release_year_with_incorrect_inputs(client):
    # Attempt to search with wrong release year
    response = client.post(
        '/search/1',
        data={
            'id': 1996
            }
    )
    # Check that supplying incorrect data with the right type redirects the data to be handled elsewhere.
    assert response.status_code == 302
    
    # Attempt to search with no release year
    response = client.post(
        '/search/1'
    )
    # Check that supplying no data returns the form with an additional message
    assert response.status_code == 200
    assert b"Invalid Input/s" in response.data
    

    # Attempt to search with wrong release year (Type)
    response = client.post(
        '/search/1',
        data={
            'id': "HELLO"
            }
    )
    # Check that supplying the wrong type of data returns the form with an additional message
    assert response.status_code == 200
    assert b"Invalid Input/s" in response.data

################################################################################################################

def test_search_title_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search/2')
    assert response.status_code == 200 #Redirect

    #Checking that Elements are appearing
    assert b'Title:' in response.data
    assert b'Find' in response.data
    
def test_search_title_with_correct_input(client):
    # Attempt to search with release year
    response = client.post(
        '/search/2',
        data={
            'name': "Superman Archives, Vol. 2"
            }
    )
    # Check that supplying correct data returns a result i.e. 302 Redirect.
    assert response.status_code == 302

def test_search_title_with_incorrect_inputs(client):
    # Attempt to search with wrong title year
    response = client.post(
        '/search/2',
        data={
            'name': "HAHAHAHAHA"
            }
    )
    # Check that supplying incorrect data with the right type redirects the data to be handled elsewhere.
    assert response.status_code == 302
    
    # Attempt to search with no title
    response = client.post(
        '/search/2',
        data={
            'name': None
        }
    )
    response_1 = client.post(
        '/search/2'
    )
    # Check that supplying no data returns the form with an additional message
    assert response.status_code == 302
    assert response_1.status_code == 302
    

    # Attempt to search with wrong release year (Type)
    response = client.post(
        '/search/2',
        data={
            'name': 9999999
            }
    )
    # Check that supplying the wrong type of data returns the form with an additional message
    assert response.status_code == 302

################################################################################################################

def test_search_publisher_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search/3')
    assert response.status_code == 200 #Redirect

    #Checking that Elements are appearing
    assert b'Publisher Name:' in response.data
    assert b'Find' in response.data
    
def test_search_publisher_with_correct_input(client):
    # Attempt to search with release year
    response = client.post(
        '/search/3',
        data={
            'name': "DC Comics"
            }
    )
    # Check that supplying correct data returns a result i.e. 302 Redirect.
    assert response.status_code == 302

def test_search_publisher_with_incorrect_inputs(client):
    # Attempt to search with wrong publisher name
    response = client.post(
        '/search/3',
        data={
            'name': "Derp"
            }
    )
    # Attempt to search with no publisher name
    response_1 = client.post(
        '/search/3',
        data={
            'name': None
        }
    )
    response_2 = client.post(
        '/search/3'
    )
    # Attempt to search with wrong publisher name (Type)
    response_3 = client.post(
        '/search/3',
        data={
            'name': 9999999
            }
    )
    # Check that supplying incorrect data redirects the data to be handled elsewhere.
    assert response.status_code == 302
    assert response_1.status_code == 302
    assert response_2.status_code == 302
    assert response_3.status_code == 302

################################################################################################################

def test_search_book_id_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search/4')
    assert response.status_code == 200 #Redirect

    #Checking that Elements are appearing
    assert b'Book id:' in response.data
    assert b'Find' in response.data
    
def test_search_book_id_with_correct_input(client):
    # Attempt to search with release year
    response = client.post(
        '/search/4',
        data={
            'book_id': 707611
            }
    )
    # Check that supplying correct data returns a results
    assert response.status_code == 200

def test_search_book_id_with_incorrect_inputs(client):
    # Attempt to search with wrong release year
    response = client.post(
        '/search/4',
        data={
            'id': 1996
            }
    )
    # Check that supplying incorrect data with the right type redirects the data to be handled elsewhere.
    assert response.status_code == 302
    
    # Attempt to search with no release year
    response = client.post(
        '/search/4'
    )
    # Check that supplying no data returns the form with an additional message
    assert response.status_code == 200
    assert b"Invalid Input/s" in response.data
    
    # Attempt to search with wrong release year (Type)
    response = client.post(
        '/search/4',
        data={
            'id': "HELLO"
            }
    )
    # Check that supplying the wrong type of data returns the form with an additional message
    assert response.status_code == 200
    assert b"Invalid Input/s" in response.data

################################################################################################################

def test_general_search_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/search/5')
    assert response.status_code == 200 #Redirect

    #Checking that Elements are appearing
    assert b'Author Name:' in response.data
    assert b'Author ID:' in response.data
    assert b'Release Year:' in response.data
    assert b'Title:' in response.data
    assert b'Publisher Name:' in response.data
    assert b'Book ID:' in response.data
    assert b'Search By:' in response.data
    assert b'Find' in response.data
    
def test_general_search_with_correct_input(client):
    # Attempt to search with each different type of data

    response = client.post(
        '/search/5',
        data={
            'author_name': "Katsura Hoshino",
            'searchOption':"Author"
            }
    )
    response_1 = client.post(
        '/search/5',
        data={
            'author_id': 311098,
            'searchOption':"Author ID"
            }
    )
    response_2 = client.post(
        '/search/5',
        data={
            'release_year': 1997,
            'searchOption':"Release Year"
            }
    )
    response_3 = client.post(
        '/search/5',
        data={
            'title': "Superman Archives, Vol. 2",
            'searchOption':"Title"
            }
    )
    response_4 = client.post(
        '/search/5',
        data={
            'publisher_name': "DC Comics",
            'searchOption':"Publisher"
            }
    )
    response_5 = client.post(
        '/search/5',
        data={
        'book_id': 707611,
        'searchOption':"BookID"
        }
    )

    # Check that supplying correct data returns a result i.e. 302 Redirect.
    assert response.status_code == 302
    assert response_1.status_code == 302
    assert response_2.status_code == 302
    assert response_3.status_code == 302
    assert response_4.status_code == 302
    assert response_5.status_code == 302

def test_general_search_with_incorrect_inputs(client):
    #region author_name
    response = client.post(
        '/search/5',
        data={
            'author_name': "Hello",
            'searchOption':"Author"
            }
    )
    assert response.status_code == 200

    response = client.post(
        '/search/5',
        data={
            'author_name': 1,
            'searchOption':"Author"
            }
    )
    assert response.status_code == 200

    response = client.post(
        '/search/5',
        data={
            'author_name': None,
            'searchOption':"Author"
            }
    )
    assert response.status_code == 302
    #endregion
    #region author_id
    response = client.post(
        '/search/5',
        data={
            'author_id': 1,
            'searchOption':"Author ID"
            }
    )
    assert response.status_code == 200
        
    response = client.post(
        '/search/5',
        data={
            'author_id': "Hello",
            'searchOption':"Author ID"
            }
    )
    assert response.status_code == 200

    response = client.post(
        '/search/5',
        data={
            'author_id': None,
            'searchOption':"Author ID"
            }
    )
    assert response.status_code == 302
    #endregion
    #region release_year
    response = client.post(
        '/search/5',
        data={
            'release_year': 1996,
            'searchOption':"Release Year"
            }
    )
    assert response.status_code == 302
    
    response = client.post(
        '/search/5',
        data={
            'release_year': None,
            'searchOption':"Release Year"
            }
    )
    assert response.status_code == 302

    response = client.post(
        '/search/5',
        data={
            'release_year': "HELLO",
            'searchOption':"Release Year"
            }
    )
    assert response.status_code == 302
    #endregion
    #region title
    response = client.post(
        '/search/5',
        data={
            'title': "HAHAHAHAHA",
            'searchOption':"Title"
            }
    )
    assert response.status_code == 302

    response = client.post(
        '/search/5',
        data={
            'title': 9999999,
            'searchOption':"Title"
            }
    )
    assert response.status_code == 302

    response = client.post(
        '/search/5',
        data={
            'title': None,
            'searchOption':"Title"
            }
    )
    assert response.status_code == 302
    #endregion
    #region publisher_name
    response = client.post(
        '/search/5',
        data={
            'publisher_name': "Derp",
            'searchOption':"Publisher"
            }
    )
    assert response.status_code == 200

    response = client.post(
        '/search/5',
        data={
            'publisher_name': None,
            'searchOption':"Publisher"
            }
    )
    assert response.status_code == 302

    response = client.post(
        '/search/5',
        data={
            'publisher_name': 9999999,
            'searchOption':"Publisher"
            }
    )
    assert response.status_code == 200
    #endregion
    #region book_id
    response = client.post(
        '/search/5',
        data={
        'book_id': 1996,
        'searchOption':"BookID"
        }
    )
    assert response.status_code == 302
    
    response = client.post(
        '/search/5',
        data={
        'book_id': None,
        'searchOption':"BookID"
        }
    )
    assert response.status_code == 302

    response = client.post(
        '/search/5',
        data={
        'book_id': "HELLO",
        'searchOption':"BookID"
        }
    )
    assert response.status_code == 302
    #endregion

################################################################################################################
#   TESTS FOR SEARCH QUERIES                                                                                   
################################################################################################################

def test_book_by_book_id_without_book_id(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/4/query?book_id=',follow_redirects=True)
    assert response.status_code == 404

    response_1 = client.get('/search/4/query',follow_redirects=True)
    assert response_1.status_code == 404

    #Check that without a provided date, the page shows a 404 Error
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_book_id_with_book_id(client):
    #Check that we can retrieve the book page.
    response = client.get('/search/4/query?book_id=11827783',follow_redirects=True)
    assert response.status_code == 200
    
    #Check that books have been retrieved correctly
    assert b'Sherlock Holmes: Year One' in response.data

def test_book_by_book_id_with_invalid_book_id(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/4/query?book_id=999999',follow_redirects=True)
    response = client.get('/search/4/query?book_id=9.99999',follow_redirects=True)
    response_1 = client.get('/search/4/query?book_id=SOMANYTESTS',follow_redirects=True)

    assert response.status_code == 404
    assert response.status_code == 404
    assert response_1.status_code == 404

    #Check that error books have been retrieved correctly
    assert b'404' in response.data
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_book_id_with_review(client):
    # Check that we can retrieve the books page.
    response = client.get('/search/4/query?book_id=707611',follow_redirects=True)
    assert response.status_code == 200
    
    # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data

################################################################################################################

def test_book_by_title_without_title(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/2/query?title=')
    assert response.status_code == 404

    response_1 = client.get('/search/2/query')
    assert response_1.status_code == 404

    #Check that without a provided date, the page shows a 404 Error
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_title_with_title(client):
    #Check that we can retrieve the book page.
    response = client.get('/search/2/query?title=Sherlock Holmes: Year One',follow_redirects=True)
    assert response.status_code == 200

    #Check that books have been retrieved correctly
    assert b'Sherlock Holmes: Year One' in response.data

def test_book_by_title_with_invalid_title(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/2/query?title=999999',follow_redirects=True)
    response_1 = client.get('/search/2/query?title=ANOTHERTEST',follow_redirects=True)

    assert response.status_code == 404
    assert response_1.status_code == 404

    #Check that error books have been retrieved correctly
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_title_with_review(client):
    # Check that we can retrieve the books page.
    response = client.get('/search/2/query?title=Superman+Archives%2C+Vol.+2',follow_redirects=True)
    assert response.status_code == 200
    
    # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data
    
################################################################################################################

def test_book_by_author_id_without_author_id(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/0/0/query?author_id=')
    assert response.status_code == 404

    response_1 = client.get('/search/0/0/query')
    assert response_1.status_code == 404

    #Check that without a provided date, the page shows a 404 Error
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_author_id_with_author_id(client):
    #Check that we can retrieve the book page.
    response = client.get('/search/0/0/query?author_id=4980321',follow_redirects=True)
    assert response.status_code == 200
    #Check that we can retrieve multiple books in a table
    response_1 = client.get('/search/0/0/query?author_id=294649')
    assert response_1.status_code == 200
    #Check that books have been retrieved correctly
    assert b'Sherlock Holmes: Year One' in response.data
    assert b"12349663" in response_1.data
    assert b"12349665" in response_1.data  

def test_book_by_author_id_with_invalid_author_id(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/0/0/query?author_id=27182818284590452353602874713527')
    response = client.get('/search/0/0/query?author_id=2.7182818284590452353602874713527')
    response_1 = client.get('/search/0/0/query?author_id=LoremIpsum')

    assert response.status_code == 404
    assert response.status_code == 404
    assert response_1.status_code == 404

    #Check that error books have been retrieved correctly
    assert b'404' in response.data
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_author_id_with_review(client):
    # Check that we can retrieve the books page.
    response = client.get('/search/0/0/query?author_id=81563',follow_redirects=True)
    assert response.status_code == 200
    
    # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data

################################################################################################################

def test_book_by_author_name_without_author_name(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/0/1/query?author_name=')
    assert response.status_code == 404

    response_1 = client.get('/search/0/1/query')
    assert response_1.status_code == 404

    #Check that without a provided date, the page shows a 404 Error
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_author_name_with_author_name(client):
    #Check that we can retrieve the book page.
    response = client.get('/search/0/1/query?author_name=Daniel+Indro',follow_redirects=True)
    assert response.status_code == 200
    #Check that we can retrieve multiple books in a table
    response_1 = client.get('/search/0/1/query?author_name=Naoki+Urasawa')
    assert response_1.status_code == 200
    #Check that books have been retrieved correctly
    assert b'Sherlock Holmes: Year One' in response.data
    assert b"12349663" in response_1.data
    assert b"12349665" in response_1.data  

def test_book_by_author_name_with_invalid_author_name(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/0/0/query?author_name=27182818284590452353602874713527')
    response = client.get('/search/0/0/query?author_id=LoremIpsum')

    assert response.status_code == 404
    assert response.status_code == 404
    
    #Check that error books have been retrieved correctly
    assert b'404' in response.data
    assert b'404' in response.data

def test_book_by_author_name_with_review(client):
    # Check that we can retrieve the books page.
    response = client.get('/search/0/1/query?author_name=Jerry+Siegel',follow_redirects=True)
    assert response.status_code == 200
    
    # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data
    
################################################################################################################

def test_book_by_author_nameid_without_author_nameid(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/0/2/query?author_id=&author_name=')
    assert response.status_code == 404

    response_1 = client.get('/search/0/2/query')
    assert response_1.status_code == 404

    #Check that without a provided date, the page shows a 404 Error
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_author_nameid_with_author_nameid(client):
    #Check that we can retrieve the book with same id and author.
    response = client.get('/search/0/2/query?author_id=93069&author_name=Rich+Tommaso',follow_redirects=True)
    assert response.status_code == 200
    
    #Check that we can retrieve the book with right id and wrong author.
    response_1 = client.get('/search/0/2/query?author_id=93069&author_name=wrong',follow_redirects=True)
    assert response_1.status_code == 200
    
    #Check that we can retrieve the book with wrong id and right author.
    response_2 = client.get('/search/0/2/query?author_id=9301231231239&author_name=Rich+Tommaso',follow_redirects=True)
    assert response_2.status_code == 200

    #Check that we can retrieve multiple books in a table with same id and author
    response_3 = client.get('/search/0/2/query?author_name=Naoki+Urasawa&author_id=294649')
    assert response_3.status_code == 200

    #Check that we can retrieve multiple books in a table with different ids and authors
    response_4 = client.get('/search/0/2/query?author_id=8551671&author_name=Rich+Tommaso')
    assert response_4.status_code == 200

    #Check that books have been retrieved correctly
    assert b'She Wolf #1' in response.data
    assert b'She Wolf #1' in response_1.data
    assert b'She Wolf #1' in response_2.data
    assert b'12349663' in response_3.data
    assert b'12349665' in response_3.data
    assert b'25742454' in response_4.data
    assert b'30735315' in response_4.data
def test_book_by_author_nameid_with_invalid_author_nameid(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/0/2/query?author_id=930613213&author_name=wrong')
    assert response.status_code == 404
    
    #Check that error has been retrieved correctly
    assert b'404' in response.data

def test_book_by_author_nameid_with_missing_arg(client):
    #Check that we can get an book with a missing arg
    response = client.get('/search/0/2/query?author_id=61231',follow_redirects=True)
    assert response.status_code == 200
    response_1 = client.get('/search/0/2/query?author_name=Scott+Beatty',follow_redirects=True)
    assert response_1.status_code == 200
    
    #Check that book has been retrieved correctly
    assert b'Sherlock Holmes: Year One' in response.data
    assert b'Sherlock Holmes: Year One' in response_1.data

def test_book_by_author_nameid_with_missing_arg_and_invalid_author_name_id(client):
    #Check that we can get an error response with a missing arg and other arg invalid
    response = client.get('/search/0/2/query?author_id=930613213')
    assert response.status_code == 404
    response_1 = client.get('/search/0/2/query?author_id=PLEASENOMORETESTS')
    assert response_1.status_code == 404
    response_2 = client.get('/search/0/2/query?author_name=PLEASENOMORETESTS')
    assert response_2.status_code == 404
    response_3 = client.get('/search/0/2/query?author_name=874527865694326543879643')
    assert response_3.status_code == 404

    #Check that error has been retrieved correctly
    assert b'404' in response.data
    assert b'404' in response_1.data
    assert b'404' in response_2.data
    assert b'404' in response_3.data

def test_book_by_author_nameid_with_review(client):
    # Check that we can retrieve the book
    response = client.get('/search/0/2/query?author_name=Jerry+Siegel&author_id=89537',follow_redirects=True)
    assert response.status_code == 200
    
    # # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data

################################################################################################################

def test_book_by_publisher_without_publisher(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/3/query?publisher_name=')
    assert response.status_code == 404

    response_1 = client.get('/search/3/query')
    assert response_1.status_code == 404

    #Check that without a provided date, the page retrieves books without release years
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_publisher_with_publisher(client):
    #Check that we can retrieve the book page.
    response = client.get('/search/3/query?publisher_name=Go%21+Comi',follow_redirects=True)
    assert response.status_code == 200
    #Check that we can retrieve multiple books in a table
    response_1 = client.get('/search/3/query?publisher_name=N.A.')
    assert response_1.status_code == 200

    # #Check that books have been retrieved correctly
    # assert b'2250580' in response.data
    assert b'18955715' in response_1.data
    assert b'23272155' in response_1.data   

def test_book_by_publisher_with_invalid_publisher(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/3/query?publisher_name=HAHAHA')
    response_1 = client.get('/search/3/query?publisher_name=99999')
    assert response.status_code == 404

    #Check that error books have been retrieved correctly
    assert b'404' in response.data
    assert b'404' in response_1.data

def test_book_by_publisher_with_review(client):
    # Check that we can retrieve the books page.
    response = client.get('/search/3/query?publisher_name=DC+Comics',follow_redirects=True)
    assert response.status_code == 200

    # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data

################################################################################################################

def test_book_by_date_without_date(client):
    #Check that we can retrive the books with no release years
    response = client.get('/search/1/query?release_year=')
    assert response.status_code == 200

    response_1 = client.get('/search/1/query')
    assert response_1.status_code == 200

    #Check that without a provided date, the page retrieves books without release years
    assert b'Katsura Hoshino' in response.data
    assert b'The Switchblade Mamma' in response_1.data

def test_book_by_date_with_date(client):
    #Check that we can retrieve the book page.
    response = client.get('/search/1/query?release_year=2014',follow_redirects=True)
    assert response.status_code == 200
    #Check that we can retrieve multiple books in a table
    response_1 = client.get('/search/1/query?release_year=2016')
    assert response_1.status_code == 200

    #Check that books have been retrieved correctly
    assert b'The Breaker New Waves, Vol 11' in response.data
    assert b'War Stories, Volume 4' in response_1.data
    assert b'Cruelle' in response_1.data   

def test_book_by_date_with_invalid_date(client):
    #Check that we can get an error response with an invalid request
    response = client.get('/search/1/query?release_year=THISISERRORTEXT')
    assert response.status_code == 404

    #Check that error books have been retrieved correctly
    assert b'404' in response.data

def test_book_by_date_with_review(client):
    # Check that we can retrieve the books page.
    response = client.get('/search/1/query?release_year=1997',follow_redirects=True)
    assert response.status_code == 200

    # Check that all reviews for specified book are included on the page.
    assert b'TestTestTestTestTestTest' in response.data

