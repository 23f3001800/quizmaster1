
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db=SQLAlchemy()

class Users(db.Model):
    __tablename__="Users"

    id=db.Column(db.Integer, primary_key=True, unique=True)
    full_name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    qualification=db.Column(db.String(100), nullable=False)
    dob=db.Column(db.Date, nullable=False)
    role=db.Column(db.Integer, default=1, nullable=False)
    status=db.Column(db.String(100), default="Active",nullable=False)
    Score=db.relationship('Scores', backref='Users', cascade="all, delete-orphan")

class Subjects(db.Model):
    __tablename__="Subjects"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(100), nullable=False)
    chapter=db.relationship("Chapters", backref='Subjects', cascade="all, delete-orphan")

class Chapters(db.Model):
    __tablename__="Chapters"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(100), nullable=False)
    subject_id=db.Column(db.Integer, db.ForeignKey("Subjects.id", ondelete="CASCADE"), nullable=False)
    quiz=db.relationship('Quizzes', backref="Chapters", cascade="all, delete-orphan")



class Quizzes(db.Model):
    __tablename__="Quizzes"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title=db.Column(db.String(100), nullable=False)
    Chapter_id=db.Column(db.Integer, db.ForeignKey('Chapters.id',ondelete="CASCADE"))
    total_score=db.Column(db.Integer, default=100, nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    time_duration=db.Column(db.String(11), nullable=False)
    remark=db.Column(db.String(100))
    status=db.Column(db.String(100),default="Active", nullable=False)
    Question=db.relationship('Questions', backref="Quizzes", cascade="all, delete-orphan")
    Score=db.relationship('Scores', backref='Quizzes', cascade="all, delete-orphan")


class Questions(db.Model):
    __tablename__="Questions"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title=db.Column(db.String(100),nullable=False)
    question=db.Column(db.String(100), nullable=False)
    option1=db.Column(db.String(100), nullable=False)
    option2=db.Column(db.String(100), nullable=False)
    option3=db.Column(db.String(100), nullable=False)
    option4=db.Column(db.String(100), nullable=False)
    answer=db.Column(db.String(100), nullable=False)
    Quiz_id=db.Column(db.Integer, db.ForeignKey('Quizzes.id', ondelete="CASCADE"), nullable=False)
    marks=db.Column(db.Integer, default=10,nullable=False)


class Scores(db.Model):
    __tablename__="Scores"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True , unique=True)
    user_id=db.Column(db.Integer, db.ForeignKey('Users.id', ondelete="CASCADE"))
    Quiz_id=db.Column(db.Integer, db.ForeignKey('Quizzes.id', ondelete="CASCADE"))
    time_taken=db.Column(db.Float)
    q_attempt=db.Column(db.Integer)
    score=db.Column(db.Integer, nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_score=db.Column(db.Boolean, default=False, nullable=False)






