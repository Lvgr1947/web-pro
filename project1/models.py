from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

# db = SQLAlchemy()
Base = declarative_base()

class USER(Base):
   __tablename__ = 'user'
   username = Column(String(50), primary_key=True)
   password = Column(String(50))  
   timestamp = Column(Integer, nullable=False) 
   def __init__(self, username, password, timestamp):
      self.username = username
      self.password = password
      self.timestamp = timestamp
   def __repr__(self):
      return '<USER %r>' % (self.username)

class BOOK(Base):
   __tablename__ = 'book'
   isbn = Column(String(50), primary_key=True)
   bname = Column(String(50))  
   author = Column(String(50)) 
   year = Column(String(50))
   def __init__(self, isbn, bname, author, year):
      self.isbn = isbn
      self.bname = bname
      self.author = author
      self.year = year
   def __repr__(self):
      return '<BOOK %r>' % (self.isbn)


# class RATING(Base):
#    __tablename__ = 'rating'
#    isbn = Column(String(50), foreign_key=True)
#    username = Column(String(50), foreign_key=True)
#    rating = Column(String(50))
#    review = Column(String(200))
#    def __init__(self, isbn, username, rating, review):
#       self.isbn = isbn
#       self.username = username
#       self.rating = rating
#       self.review = review
#    def __repr__(self):
#       return '<RATING %r>' % (self.username)