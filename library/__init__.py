"""Initialize Flask app."""
import os
from flask import Flask, url_for, request,send_from_directory

# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import library.adapters.repository as repo
from library.adapters import memory_repository, database_repository, repository_populate
from library.adapters.memory_repository import populate#, populate_books
from library.adapters.orm import metadata, map_model_to_tables

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # repo.repo_instance = repo.MemoryRepository(
    # )
    print('\033[95m'+"\nThere may be some offensive words in the reviews/Usernames/passwords\nthat may not have been filtered when the files were generated from files \ncontaining common passwords and usernames.\n"+"There is not meant to be any offensive material in this project\n".upper()+'\033[0m')
    if test_config is not None:
        app.config.from_mapping(test_config)
        tests = True
        # populate(repo.repo_instance,"tests")
    else:
        # populate(repo.repo_instance)
        tests = False
        
    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        if tests:
            repository_populate.populate(repo.repo_instance, "test_folder\\tests")
        else:
            repository_populate.populate(repo.repo_instance,"library\\adapters")


    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            if app.config['TESTING'] == 'True':
                repository_populate.populate(repo.repo_instance,'tests', database_mode)
            else:
                repository_populate.populate(repo.repo_instance,'library\\adapters', database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
    
    with app.app_context():
        from .books import book
        app.register_blueprint(book.book_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
        
    return app

