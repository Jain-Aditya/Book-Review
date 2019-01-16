from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "user" 
    username = db.Column(db.String,nullable=False,primary_key=True)
    password = db.Column(db.String,nullable=False)

class Book(db.Model):
    __tablename__ = "book"
    isbn = db.Column(db.String,nullable=False,primary_key=True)
    title = db.Column(db.String,nullable=False)
    author = db.Column(db.String,nullable=False)
    year = db.Column(db.String,nullable=False)
    reviews = db.relationship("Reviews", backref="book", lazy=True)

class Reviews(db.Model):
    __tablename__="review"
    review_id = db.Column(db.Integer,nullable=False,primary_key=True)
    review_text = db.Column(db.String,nullable=True)
    book_isbn = db.Column(db.String,db.ForeignKey("book.isbn"),nullable=False)    
