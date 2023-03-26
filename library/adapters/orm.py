from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import interfaces, mapper, relation, relationship, synonym,registry
from sqlalchemy.sql.expression import column, false

from library.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, unique=True, autoincrement=True),
    Column('user_name', String(255), primary_key=True),
    Column('password', String(255), nullable=False),
    Column('reading_list',ForeignKey('books.id'),nullable=True)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('review_text', String(1024), nullable=False,default=""),
    Column('rating', Integer,nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('book_id', ForeignKey('books.id')),
    Column('user_name', ForeignKey('users.user_name'))
    
)

publishers_table = Table(
    'publishers',metadata,
    Column('name', String(1024), primary_key=True,default="N.A."),
    Column('id', Integer,nullable=True,default=0,autoincrement=True)
)

authors_table = Table(
    'authors',metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(1024), nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('release_year', Integer, default=0),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=True),
    Column('publisher_name',ForeignKey('publishers.name'))
)
books_authors_table = Table(
    'books_authors',metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id'))

)
user_reading_list_table = Table(
    'user_reading_list',metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id',ForeignKey('books.id')),
    Column('user_id',ForeignKey('users.id'))
)
def map_model_to_tables():
    mapper_registry = registry()
    mapper_registry.map_imperatively(model.User, users_table, properties={
        '_User__user_id': users_table.c.id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reading_list':relationship(model.Book,secondary=user_reading_list_table,back_populates="_Book__users"),
        '_User__reviews': relationship(model.Review)#, backref='_Review__user_associated')#,back_populates="_Re")
    })
    mapper_registry.map_imperatively(model.Review, reviews_table, properties={
        
        '_Review__id': reviews_table.c.id,
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating':reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__book':relationship(model.Book,back_populates='_Book__reviews'),
        '_Review__user_associated':relationship(model.User,back_populates="_User__reviews")

    })
    mapper_registry.map_imperatively(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,
        '_Publisher__publisher_id': publishers_table.c.id,
        '_Publisher__books': relationship(model.Book,back_populates='_Book__publisher')
        
    })
    
    mapper_registry.map_imperatively(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__release_year': books_table.c.release_year,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': relationship(model.Publisher,back_populates="_Publisher__books",viewonly=True),
        '_Book__authors': relationship(model.Author,secondary=books_authors_table,back_populates='_Author__books'),
        '_Book__users':relationship(model.User,secondary=user_reading_list_table,back_populates='_User__reading_list'),
        '_Book__reviews':relationship(model.Review,back_populates='_Review__book')
        
    })
    mapper_registry.map_imperatively(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__author_full_name': authors_table.c.name,
        '_Author__books': relationship(
            model.Book,
            secondary=books_authors_table,
            back_populates="_Book__authors"
        )
    })
