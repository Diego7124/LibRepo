from config.db import db

class Member(db.Model):
    __tablename__ = 'members'
    MemberID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.String(20), nullable=False, unique=True)
    FirstName = db.Column(db.String(50), nullable = False)
    LastName  = db.Column(db.String(50), nullable = False)
    Email = db.Column(db.String(50), nullable = False)
    PhoneNumber = db.Column(db.String(20), nullable = False)
    