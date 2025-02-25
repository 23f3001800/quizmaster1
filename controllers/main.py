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
        user=User.query.filter_by(email=uname).first()
        new_user=User(full_name=fname,email=uname,password=password, qualification=quali,dob=dob)
        if user:
            return render_template('signup.html', again=True, msg='user already exixts')
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",msg="ragistration succesful")
    
    return render_template("signup.html", msg="")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        uname=request.form.get('user_name')
        password=request.form.get('password')
        user=User.query.filter_by(email=uname,password=password).first()
        if user and user.role==0:
            return redirect(url_for('admin_dashboard',name=uname))
        elif user and user.role==1:
            return redirect(url_for("user_dashboard",name=uname))
        else:
            return render_template('login.html', msg='invalid user')
    return render_template("login.html", msg="")
        
@app.route("/admin_dashboard/<name>")
def admin_dahboard(name):
    subjects=Subject.query.all()
    return render_template("admindashboard.html", name=name, subjects=subjects)

@app.route("/new_subject" ,methods=["GET","POST"])
def new_subject():
    if request.method=="POST":
        subjects=Subject.query.all()
        new_subject=request.form.get("new_subject")
        desc=request.form.get('desc')
        subject=Subject(name=new_subject,description=desc)
        if subject in subjects:
            return render_template('newsubject.html', msg='subject already exists')
        db.session.add(subject)
        db.session.commit()
        return render_template('admin_dahboard', msg='subject added succesfully')
    return render_template("newsubject.html", msg='')

@app.route("/new_chapter/<subject>" ,methods=["GET","POST"])
def new_chapter(subject):
    if request.method=="POST":
        chapters=Chapter.query.all()
        new_chapter=request.form.get('newchapter')
        desc=request.form.get('description')
        chapter=Chapter(name=new_chapter,description=desc)
        if chapter in chapters:
            return render_template('newchapter.html', msg='chapter already exists')
        db.session.add(chapter)
        db.session.commit()
        return render_template('admin_dashboard')
    return render_template("newchapter.html", msg='',subject=subject)

@app.route("/new_question/<chapter_id>" ,methods=["GET","POST"])
def new_question(chapter_id):
    if request.method=="POST":
        qtit=request.form.get()
        qes=request.form.get('description')
        o1=request.form.get()
        o2=request.form.get()
        o3=request.form.get()
        o4=request.form.get()
        ans=request.form.get()
        question=Question(chapter_id=chapter_id,title=qtit,question=qes,option1=o1, option2=o2,option3=o3,option4=o4,answer=ans )
        
        db.session.add(question)
        db.session.commit()
    return render_template("newquestion.html" , chapter_id=chapter_id)

@app.route("/new_quiz/<chapter_id>" ,methods=["GET","POST"])
def new_quiz(chapter_id):
    if request.method=="POST":
        chapter=Chapter.query.filter_by(chapter_id)

        title=request.form.get('newchapter')
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

@app.route("/user_dashboard/<name>" ,methods=["GET","POST"])
def user_dashboard(name):
    quizzes=Quiz.query.all()
    return render_template("user_dashboard.html",name=name,quizzes=quizzes)

@app.route("/view_quiz/<quiz_id>" ,methods=["GET","POST"])
def view_score(quiz_id):
    quiz=Quiz.query.filter_by(quiz_id)
    return render_template("view.html",quiz=quiz)

@app.route("/scores" ,methods=["GET","POST"])
def scores():
    return render_template("scores.html")




    

if __name__=="__main__":
    app.run(debug=True)
