from os import error
from wtforms.fields.simple import HiddenField

from wtforms.form import Form
from wtforms.widgets.core import HiddenInput
from library.authentication.authentication import register
from flask import Flask,Blueprint, render_template, url_for, request,redirect,session
from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,SelectField,StringField,validators
from wtforms.validators import DataRequired
from flask.wrappers import Request

import library.adapters.repository as repo
import library.utilities.utilities as utilities

search_blueprint = Blueprint(
    'search_bp',__name__,url_prefix='/search'
)

@search_blueprint.route('/')
def search_interface():
    if session.get('logged_in'):
        return render_template('home/search_home.html',
        list_url = utilities.get_list_url(),
        search_url = utilities.get_search_url(),
        register_url = utilities.get_register_url(),
        logout_url= utilities.get_logout_url(),
        login_url = utilities.get_login_url(),
        recommendations = repo.repo_instance.get_recommendations(session['user_name'])
        )
    else:
        return render_template('home/search_home.html',
        list_url = utilities.get_list_url(),
        search_url = utilities.get_search_url(),
        register_url = utilities.get_register_url(),
        logout_url= utilities.get_logout_url(),
        login_url = utilities.get_login_url(),
        recommendations = repo.repo_instance.get_recommendations()
        )

@search_blueprint.route('/<int:arg>/',methods=['GET','POST'])
@search_blueprint.route('/<int:arg>',methods=['GET','POST'])
def search_book(arg):
    basic_form = GeneralSearchForm()
    precision_form = PrecisionSearchForm()
    data = None
    if request.method == "POST":
        if arg == 0:    #Author    
            if basic_form.validate_on_submit():
                ID = True
                Name = True

                try:
                    if basic_form.author_id.data == None:
                        raise TypeError
                    author_id = int(basic_form.author_id.data)
                except TypeError:
                    ID = False
                    author_id = None

                try:
                    if str(basic_form.author_name.data) == "":
                        raise TypeError
                    author_name = str(basic_form.author_name.data)
                except TypeError:
                    Name = False
                    author_name = None

                if not ID and not Name:
                    data = "Invalid Input/s, \n Please Try Again"
                elif ID and not Name:
                    return redirect(url_for('search_bp.author_id_handler',author_id=author_id))
                elif not ID and Name:
                    return redirect(url_for('search_bp.author_name_handler',author_name=author_name))
                else:
                    return redirect(url_for('search_bp.author_name_id_handler',author_id=author_id,author_name=author_name))
            else:
                data = "Invalid Input/s, \n Please Try Again"
        elif arg == 1:  #Release Year
            if basic_form.validate_on_submit():
                try:
                    if basic_form.id.data == None:
                        raise TypeError
                    release_year = int(basic_form.id.data)
                except TypeError:
                    data = "Invalid Input/s, \n Please Try Again"
                else:
                    return redirect(url_for('search_bp.release_year_handler',release_year=release_year))
            else:
                data = "Invalid Input/s, \n Please Try Again"
        elif arg == 2:  #title
            if basic_form.validate_on_submit():
                try:
                    if basic_form.name.data == "":
                        raise TypeError
                    title = str(basic_form.name.data)
                except TypeError:
                    data = "Invalid Input/s, \n Please Try Again"
                else:
                    return redirect(url_for('search_bp.title_handler',title=title))
            else:
                data = "Invalid Input/s, \n Please Try Again"
        elif arg == 3:  #Publisher
            if basic_form.validate_on_submit():
                try:
                    if basic_form.publisher_name.data == "":
                        raise TypeError
                    publisher_name = str(basic_form.publisher_name.data)
                except TypeError:
                    data = "Invalid Input/s, \n Please Try Again"
                else:
                    return redirect(url_for('search_bp.publisher_handler',publisher_name=publisher_name))
            else:
                data = "Invalid Input/s, \n Please Try Again"
        elif arg == 4:  #book_id     
            if basic_form.validate_on_submit():
                try:
                    if basic_form.id.data == None:
                        raise TypeError
                    book_id = int(basic_form.id.data)
                except TypeError:
                    data = "Invalid Input/s, \n Please Try Again"
                else:
                    return redirect(url_for('search_bp.book_id_handler',book_id = book_id))
            else:
                data = "Invalid Input/s, \n Please Try Again"
        elif arg == 5:
            if basic_form.validate_on_submit():
                search_option = str(precision_form.searchOption.data)
                if search_option == "Author":
                    return redirect(url_for('search_bp.author_name_handler',author_name = precision_form.author_name.data))
                if search_option =="Author ID":
                    return redirect(url_for('search_bp.author_id_handler',author_id = precision_form.author_id.data))
                if search_option =="Release Year":
                    return redirect(url_for('search_bp.release_year_handler',release_year = precision_form.release_year.data))
                if search_option =="Title":
                    return redirect(url_for('search_bp.title_handler',title = precision_form.title.data))
                if search_option =="Publisher":
                    return redirect(url_for('search_bp.publisher_handler',publisher_name = precision_form.publisher_name.data))
                if search_option =="BookID":
                    return redirect(url_for('search_bp.book_id_handler',book_id = precision_form.book_id.data))
            else:
                data = "Invalid Input/s, \n Please Try Again"
                
    if arg in range(0,5):
        if session.get('logged_in'):
            return render_template('books/basic_search_form.html',
                form=basic_form,
                handler_url=url_for('search_bp.search_book',arg=arg),
                list_url = utilities.get_list_url(),
                search_url = utilities.get_search_url(),
                register_url = utilities.get_register_url(),
                logout_url= utilities.get_logout_url(),
                login_url = utilities.get_login_url(),
                data=data, search_type=arg,
                recommendations = repo.repo_instance.get_recommendations(session['user_name'])
                )
        else:
            return render_template('books/basic_search_form.html',
                form=basic_form,
                handler_url=url_for('search_bp.search_book',arg=arg),
                list_url = utilities.get_list_url(),
                search_url = utilities.get_search_url(),
                register_url = utilities.get_register_url(),
                logout_url= utilities.get_logout_url(),
                login_url = utilities.get_login_url(),
                data=data, search_type=arg,
                recommendations = repo.repo_instance.get_recommendations()
                )
    elif arg == 5:
        if session.get('logged_in'):
            return render_template('books/basic_search_form.html',
                form=precision_form,
                handler_url=url_for('search_bp.search_book',arg=arg),
                list_url = utilities.get_list_url(),
                search_url = utilities.get_search_url(),
                register_url = utilities.get_register_url(),
                logout_url= utilities.get_logout_url(),
                login_url = utilities.get_login_url(),
                data=data, search_type=arg,
                recommendations = repo.repo_instance.get_recommendations(session['user_name'])
                
                )
        else:
            return render_template('books/basic_search_form.html',
                form=precision_form,
                handler_url=url_for('search_bp.search_book',arg=arg),
                list_url = utilities.get_list_url(),
                search_url = utilities.get_search_url(),
                register_url = utilities.get_register_url(),
                logout_url= utilities.get_logout_url(),
                login_url = utilities.get_login_url(),
                data=data, search_type=arg,
                recommendations = repo.repo_instance.get_recommendations()
                
                )

@search_blueprint.route('/0/0/query')
def author_id_handler():
    if request.args.get('author_id') and request.args.get('author_id').isnumeric():
        author_id = int(request.args.get('author_id'))
    else:
        author_id = None
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1
    return search_handler_renderer(repo.repo_instance.get_books_by_author_id(author_id),page)
    
@search_blueprint.route('/0/1/query')
def author_name_handler():
    if request.args.get('author_name'):
        author_name = request.args.get('author_name')
    else:
        author_name = None
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1
    return search_handler_renderer(repo.repo_instance.get_books_by_author_name(author_name),page)
    
@search_blueprint.route('/0/2/query')
def author_name_id_handler():
    if request.args.get('author_name'):
        author_name = request.args.get('author_name')
    else:
        author_name = None
    if request.args.get('author_id') and request.args.get('author_id').isnumeric():
        author_id = int(request.args.get('author_id'))
    else:
        author_id = None
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1
    books = set(repo.repo_instance.get_books_by_author_name(author_name))
    for book in repo.repo_instance.get_books_by_author_id(author_id):
        books.add(book)
    books = sorted(list(books))
    return search_handler_renderer(books,page)

@search_blueprint.route('/1/query')
def release_year_handler():
    if request.args.get('release_year') and request.args.get('release_year').isnumeric():
        release_year = int(request.args.get('release_year'))
    else:
        release_year = request.args.get('release_year')
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1
    return search_handler_renderer(repo.repo_instance.get_books_by_release_year(release_year),page)
    
@search_blueprint.route('/2/query')
def title_handler():
    if request.args.get('title'):
        title = request.args.get('title')
    else:
        title = None
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1
    return search_handler_renderer(repo.repo_instance.get_book_by_title_general(title),page)
    
@search_blueprint.route('/3/query')
def publisher_handler():
    if request.args.get('publisher_name'):
        publisher_name = request.args.get('publisher_name')
    else:
        publisher_name = None
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1
    return search_handler_renderer(repo.repo_instance.get_books_by_publisher_name(publisher_name),page=page)
    
@search_blueprint.route('/4/query')
def book_id_handler():
    if request.args.get('book_id') and request.args.get('book_id').isnumeric():
        book_id = int(request.args.get('book_id'))
    else:
        book_id = None
    return redirect(url_for('book_bp.show_book',
        book_id= book_id      
    ))

def search_handler_renderer(books,page):
    if len(books)==1:
        return redirect(url_for('book_bp.show_book',
            book_id= books[0].book_id            
        ))
    elif len(books)==0:
        return render_template('error.html',
        error_code = 404,
        error_message = "Book Not Found"
        ),404
    else:
        NextPage = NextPageForm(request.args)
        PreviousPage = PreviousPageForm(request.args)
        
        NextPage.page.data = page +1
        NextPageData = {**request.args,**NextPage.data}
        PreviousPage.page.data = page -1
        PreviousPageData = {**request.args,**PreviousPage.data}
        return render_template('search/basic_search.html',
            list_url = utilities.get_list_url(),
            search_url = utilities.get_search_url(),
            register_url = utilities.get_register_url(),
            logout_url= utilities.get_logout_url(),
            login_url = utilities.get_login_url(),
            books=books,
            NextPage=NextPageData,
            PreviousPage=PreviousPageData,
            page = page
            )

class GeneralSearchForm(FlaskForm):
    author_name_options = repo.repo_instance.get_author_names()
    author_id_options = repo.repo_instance.get_author_ids()
    publisher_options = repo.repo_instance.get_all_publisher_names()
    id = IntegerField("ID",[validators.optional()])
    name = StringField("Names",[validators.optional()])
    author_name = SelectField("Author Name:",[validators.optional()],choices=author_name_options)
    author_id = SelectField("Author ID:",[validators.optional()],choices=author_id_options)
    publisher_name = SelectField("Publisher Name:",[validators.optional()],choices=publisher_options)
    submit = SubmitField("Find")

class PrecisionSearchForm(FlaskForm):
    searchOptions = ["Author","Author ID","Release Year","Title","Publisher","BookID"]
    author_name_options = repo.repo_instance.get_author_names()+[None]
    author_id_options = repo.repo_instance.get_author_ids()+[None]
    publisher_options = repo.repo_instance.get_all_publisher_names()+[None]

    book_id = IntegerField("Book ID:",[validators.optional()])
    author_name = SelectField("Author Name:",[validators.optional()],choices=author_name_options)
    author_id = SelectField("Author ID:",[validators.optional()],choices=author_id_options)
    title = StringField("Title:",[validators.optional()])
    release_year = IntegerField("Release Year:",[validators.optional()])
    publisher_name = SelectField("Publisher Name:",[validators.optional()],choices=publisher_options)
    searchOption = SelectField(label="Search By:",choices=searchOptions)
    submit = SubmitField("Find")

class NextPageForm(Form):
    page = HiddenField(widget=HiddenInput,default=1)
class PreviousPageForm(Form):
    page = HiddenField(widget=HiddenInput,default=2)
    
