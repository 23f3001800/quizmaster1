from flask import Flask, render_template,url_for, redirect,request
from flask import current_app as app
from models.database import db, User, Subject,Chapter, Question, Quiz, Score
from datetime import datetime


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        uname=request.form.get('user_name')
        password=request.form.get('password')
        fname=request.form.get('full_name')
        quali=request.form.get('qualification')
        dob=request.form.get('dob')
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
        user=User(full_name=fname,email=uname,password=password, qualification=quali,dob=dob)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        uname=request.form.get('user_name')
        password=request.form.get('password')
        user=User.query.filter_by(email=uname,password=password).first()
        if user and user.id==0:
            return redirect(url_for('admin_dashboard'))
        elif user and id==1:
            return redirect(url_for("user_dashboard"))
        else:
            return "invalid input"
    return render_template("login.html")
        
@app.route("/admin_dashboard")
def admin_dahboard():

    return render_template("admindashboard.html")

@app.route("/new_subject" ,methods=["GET","POST"])
def new_subject():
    if request.method=="POST":
        new_subject=request.form.get("new_subject")
        desc=request.form.get('desc')
        subject=Subject(name=new_subject,description=desc)
        if subject:
            return "invalid"
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_dahboard'))
    return render_template("newsubject.html")

@app.route("/new_chapter" ,methods=["GET","POST"])
def new_chapter():
    if request.method=="POST":
        new_chapter=request.form.get('newchapter')
        desc=request.form.get('description')
        chapter=Chapter(name=new_chapter,description=desc)
        if chapter:
            return "invalid"
        db.session.add(chapter)
        db.session.commit()

        return redirect(url_for('admin_dashboard'))
    return render_template("newchapter.html")

@app.route("/new_question" ,methods=["GET","POST"])
def new_question():
    if request.method=="POST":
        new_chapter=request.form.get('newchapter')
        desc=request.form.get('description')
        question=Question(name=new_chapter,description=desc)
        if question:
            return "invalid"
        db.session.add(question)
        db.session.commit()
    return render_template("user_dashboard.html")

@app.route("/new_quiz" ,methods=["GET","POST"])
def new_quiz():
    if request.method=="POST":
        new_chapter=request.form.get('newchapter')
        desc=request.form.get('description')
        quiz=Quiz(name=new_chapter,description=desc)
        if quiz:
            return "invalid"
        db.session.add(quiz)
        db.session.commit()
    return render_template("newquiz.html")

@app.route("/quiz_management" ,methods=["GET","POST"])
def quiz_management():
    return render_template("quiz_management.html")

@app.route("/user_dashboard" ,methods=["GET","POST"])
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route("/view_score" ,methods=["GET","POST"])
def view_score():
    return render_template("view.html")

@app.route("/scores" ,methods=["GET","POST"])
def scores():
    return render_template("scores.html")




    

if __name__=="__main__":
    app.run(debug=True)
