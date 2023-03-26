from flask import Blueprint,render_template,url_for,make_response,session

import library.utilities.utilities as utilities
from secrets import token_urlsafe
import library.adapters.repository as repo

home_blueprint = Blueprint(
    'home_bp',__name__
)

@home_blueprint.route('/')
def home():
    if session.get('logged_in'):
        res = make_response(render_template(
            'home/home.html',
            list_url = utilities.get_list_url(),
            search_url = utilities.get_search_url(),
            register_url = utilities.get_register_url(),
            logout_url= utilities.get_logout_url(),
            login_url = utilities.get_login_url(),
            recommendations = repo.repo_instance.get_recommendations(session['user_name'])
        )
        )
        return res,200
    else:
        res = make_response(render_template(
            'home/home.html',
            list_url = utilities.get_list_url(),
            search_url = utilities.get_search_url(),
            register_url = utilities.get_register_url(),
            logout_url= utilities.get_logout_url(),
            login_url = utilities.get_login_url(),
            recommendations = repo.repo_instance.get_recommendations()
        )
        )
        return res,200


    