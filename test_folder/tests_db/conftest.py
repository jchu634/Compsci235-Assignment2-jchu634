import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from library.adapters import database_repository, repository_populate
from library.adapters.orm import metadata, map_model_to_tables
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent

TEST_DATA_PATH_DATABASE_FULL = "library\\adapters"
TEST_DATA_PATH_DATABASE_LIMITED = "test_folder\\tests"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///library-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(repo_instance,TEST_DATA_PATH_DATABASE_LIMITED, database_mode)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(repo_instance,TEST_DATA_PATH_DATABASE_FULL, database_mode)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def session_factory_full_lite():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(repo_instance,TEST_DATA_PATH_DATABASE_FULL, database_mode,lite=True)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def session_factory_lite():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    # import logging
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    repository_populate.populate(repo_instance,TEST_DATA_PATH_DATABASE_LIMITED, database_mode)
    yield session_factory
    metadata.drop_all(engine)


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)