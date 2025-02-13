from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()

class User(db.Model):
    __tablename__="User"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    qualification=db.Column(db.String(100), nullable=False)
    dOb=db.Column(db.Date, nullable=False)
    Score=db.relationship('Score', backref='User')

class Subject(db.Model):
    __tablename__="Subject"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(100), nullable=False)
    chapter=db.relationship("Chapter", backref='Subject')

class Chapter(db.Model):
    __tablename__="Chapter"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(100), nullable=False)
    subject_id=db.Column(db.Integer, db.ForeignKey('Subject.id'), nullable=False)
    quiz=db.relationship('Quiz', backref="Chapter")


class Question(db.Model):
    __tablename__="Question"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    question=db.Column(db.String(100), nullable=False)
    option1=db.Column(db.String(100), nullable=False)
    option2=db.Column(db.String(100), nullable=False)
    option3=db.Column(db.String(100), nullable=False)
    option4=db.Column(db.String(100), nullable=False)
    answer=db.Column(db.String(100), nullable=False)
    Quiz_id=db.Column(db.Integer, db.ForeignKey('Quiz.id'), nullable=False)

class Quiz(db.Model):
    __tablename__="Quiz"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Chapter_id=db.Column(db.Integer, db.ForeignKey('Chapter.id'))
    score=db.Column(db.Integer, nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    time_duration=db.Column(db.Float, nullable=False)
    remark=db.Column(db.String(100))
    Score=db.relationship('Score', backref="Quiz")
    Question=db.relationship('Question')

class Score(db.Model):
    __tablename__="Score"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('User.id'))
    Quiz_id=db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    time_taken=db.Column(db.Float)
    total_score=db.Column(db.Integer, nullable=False)
    date=db.Column(db.Date, nullable=False)





