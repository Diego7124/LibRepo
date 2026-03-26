from config.db import db

class Book(db.Model):
    __tablename__ = 'books'
    BookID = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.String(20), nullable=False, unique=True)
    Title = db.Column(db.String(200), nullable=False)
    AuthorID = db.Column(db.Integer, db.ForeignKey('authors.AuthorID'), nullable=False)
    PublicationYear = db.Column(db.Integer, nullable=True)
    AvailableCopies = db.Column('AvailableCopies', db.Integer, nullable=False, default=0)
    TotalCopies = db.Column(db.Integer, nullable=False, default=0)