from config.db import db

class Author(db.Model):
    __tablename__ = 'authors'
    AuthorID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    BirthDate = db.Column(db.Date, nullable=True)
    Nationality = db.Column(db.String(50), nullable=True)
    books = db.relationship('Book', backref='author', lazy=True)