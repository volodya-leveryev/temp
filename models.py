from sqlalchemy import Column, Integer, String
from database import Base


# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(100), unique=False)
#     author = Column(String(100), unique=False)
#
#     def __init__(self, title=None, author=None):
#         self.title = title
#         self.author = author
#
#     def __repr__(self):
#         return '<Book %r>' % self.title
