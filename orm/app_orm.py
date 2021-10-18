from typing import List
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import FileResponse
from fastapi import FastAPI
import uvicorn
import table_orm as tao
from table_orm import Base

app = FastAPI()

engine = create_engine(
    'sqlite:///my_database.db',
    # connect_args={'check_same_thread': False},
)

@app.get("/get_author")
def get_todos():
    Session = sessionmaker(bind=engine)
    session = Session()
    list_author = session.query(tao.Author).all()
    session.close()
    return_list = []
    for au in list_author:
        return_list.append({'id': au.id, 'name': au.name})
    return return_list

@app.get("/get_book")
def get_book():
    Session = sessionmaker(bind=engine)
    session = Session()
    list_book = session.query(tao.Book).all()
    session.close()
    return_list = []
    for bo in list_book:
        return_list.append({'id': bo.id, 'name': bo.name})
    return return_list

@app.get("/get_author_book")
def get_author_book():
    Session = sessionmaker(bind=engine)
    session = Session()
    list_ab = session.query(tao.Author_book).all()
    session.close()
    return_list = []
    for ab in list_ab:
        return_list.append({'self_id': ab.id, 'author_id': ab.author_id, 'book_id': ab.book_id})
    return return_list

@app.get("/add_author") #Можно сразу передать связь нового автора с существующей книгой в БД через название
def add_author(name_add: str, book_id_add: str = None):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_row = tao.Author(name=name_add)
    session.add(new_row)
    session.commit()
    if book_id_add != None:
        new_link = tao.Author_book(author_id=new_row.id,
                                   book_id=session.query(tao.Book.id)
                                   .select_from(tao.Book).filter(tao.Book.name == book_id_add))
        session.add(new_link)
        session.commit()
    session.close()
    return {'Okey'}

@app.get("/add_book") #Можно сразу передать связь новой книги с существующим автором в БД через имя
def add_book(name_add: str, author_id_add: str = None):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_row = tao.Book(name = name_add)
    session.add(new_row)
    session.commit()
    if author_id_add != None:
        new_link = tao.Author_book(author_id=new_row.id,
                                   book_id=session.query(tao.Author.id)
                                   .select_from(tao.Author).filter(tao.Author.name == author_id_add))
        session.add(new_link)
        session.commit()
    session.close()
    return {'Okey'}

@app.get("/add_author_book")
def add_author_book(id_book: int, id_author: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_row = tao.Author_book(author_id=id_author, book_id=id_book)
    session.add(new_row)
    session.commit()
    session.close()
    return {'Okey'}

@app.get("/change_author")
def change_author(id_author: int, name_author: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    changed_record = session.query(tao.Author).get(id_author)
    changed_record.name = name_author
    session.commit()
    session.close()
    return {'Okey'}

@app.get("/change_book")
def change_book(id_book: int, name_book: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    changed_record = session.query(tao.Book).get(id_book)
    changed_record.name = name_book
    session.commit() #сохранение изменений*
    session.close()
    return {'Okey'}

@app.get("/delete_author") 
def delete_author(id_author: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(tao.Author).filter(tao.Author.id == id_author).delete()
    session.commit()
    session.close()
    return {'Okey'}

@app.get("/delete_book")
def delete_book(id_book: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(tao.Book).filter(tao.Book.id == id_book).delete()
    session.commit()
    session.close()
    return {'Okey'}

@app.get("/delete_author_book")
def delete_author_book(id_ab: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(tao.Author_book).filter(tao.Author_book.id == id_ab).delete()
    session.commit()
    session.close()
    return {'Okey'}

# Session = sessionmaker(bind=engine)
# session = Session()
# session.commit()

# print(session.query(tao.Book.id, tao.Book.name, tao.Author_book.author_id, tao.Author.name)
#       .select_from(tao.Book)
#       .join(tao.Author_book, isouter=True)
#       .join(tao.Author, isouter=True)
#       .filter(tao.Book.id == 1)
#       )


# new_row1 = table_orm.Author_book(author_id = 1, book_id = 1)
# new_row2 = table_orm.Author_book(author_id = 2, book_id = 1)
# session.add_all([new_row1, new_row2])
# Base.metadata.create_all(engine)


uvicorn.run(app, host='192.168.0.16')