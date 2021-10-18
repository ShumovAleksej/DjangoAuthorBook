import sqlalchemy as sa
from sqlalchemy import Table, Index, Integer, String, Column, Text, \
                       DateTime, Boolean, PrimaryKeyConstraint, \
                       UniqueConstraint, ForeignKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Author_book(Base):
    __tablename__ = 'Author_book'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer(), ForeignKey("authors.id"))
    book_id = Column(Integer(), ForeignKey("books.id"))

class Author(Base):
    __tablename__ = 'authors'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    book = relationship("Author_book", backref="author")

class Book(Base):
    __tablename__ = 'books'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    author = relationship("Author_book", backref="book")

# ins = Author(
#     name = 'Lev Tolstoi'
# )
