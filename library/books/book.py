from wtforms.fields.core import IntegerField
from library.authentication.authentication import login_required
from flask import Flask,Blueprint, render_template, url_for, request,redirect,session

from better_profanity import profanity

import library.utilities.utilities as utilities
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.books.services as services

book_blueprint = Blueprint(
    'book_bp', __name__
)

@book_blueprint.route('/list')
def list_books():
    if request.args.get('page') and request.args.get('page').isnumeric():
        page = int(request.args.get('page'))
    else:
        page = 1

    return render_template("books/list_books.html",
    books=repo.repo_instance.get_all_books(),
    list_url = utilities.get_list_url(),
    search_url = utilities.get_search_url(),
    register_url = utilities.get_register_url(),
    logout_url= utilities.get_logout_url(),
    login_url = utilities.get_login_url(),
    page = page
    )

@book_blueprint.route('/book',methods=['GET','POST'])
def show_book():
    if request.args.get('book_id') and request.args.get('book_id').isnumeric():
        book_id = int(request.args.get('book_id'))
    else:
        book_id = None
    try:
        if repo.repo_instance.get_book(book_id) != None:
            if session.get('logged_in'):
                return redirect(url_for('book_bp.review_book',book_id=book_id))
            else:
                book = repo.repo_instance.get_book(book_id)
                if book:
                    return render_template('search/simple_book.html',
                        book = book,
                        search_url = utilities.get_search_url(),
                        register_url = utilities.get_register_url(),
                        logout_url= utilities.get_logout_url(),
                        login_url = utilities.get_login_url(),
                        list_url = utilities.get_list_url(),
                        recommendations = repo.repo_instance.get_recommendations()
                    )
                else:
                    raise BookNotFoundError
        else:
            raise BookNotFoundError
    except BookNotFoundError:
        return render_template('error.html',
        error_code = 404,
        error_message = "Book Not Found"
        ),404

@book_blueprint.route('/review',methods=['GET','POST'])
@login_required
def review_book():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    form = ReviewForm()

    if form.validate_on_submit():
        book_id = int(form.book_id.data)
        book = repo.repo_instance.get_book(book_id)
        services.add_review(book,form.review.data,user_name,form.rating.data,repo.repo_instance)
        
        return render_template('search/simple_book.html',
                        book = book,
                        search_url = utilities.get_search_url(),
                        register_url = utilities.get_register_url(),
                        logout_url= utilities.get_logout_url(),
                        login_url = utilities.get_login_url(),
                        list_url = utilities.get_list_url(),
                        form=form,
                        recommendations = repo.repo_instance.get_recommendations(user_name)
                    )
    else:
        if request.method =='GET':
            book_id = int(request.args.get('book_id'))
            form.book_id.data = book_id
        else:
            book_id = int(form.book_id.data)
        
        book = repo.repo_instance.get_book(book_id)
        if book:

            repo.repo_instance.add_book_to_reading_list(book,user_name)
            return render_template('search/simple_book.html',
                        book = repo.repo_instance.get_book(book_id),
                        search_url = utilities.get_search_url(),
                        register_url = utilities.get_register_url(),
                        logout_url= utilities.get_logout_url(),
                        login_url = utilities.get_login_url(),
                        list_url = utilities.get_list_url(),
                        form=form,
                        recommendations = repo.repo_instance.get_recommendations(user_name)
                    )
        else:
            return render_template('error.html',
            error_code = 404,
            error_message = "Book Not Found"
            ),404


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)

class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField("Rating [1-5]",[
        DataRequired(),
        NumberRange(min=1, max=5, message='The rating must be between 1 and 5')
    ])
    book_id = HiddenField("Book id")
    submit = SubmitField('Submit')

class BookNotFoundError(Exception):
    pass