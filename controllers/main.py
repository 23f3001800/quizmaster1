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
        return render_template("login.html",msg="ragistration successful please login here")
    
    return render_template("signup.html", msg="")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        uname=request.form.get('user_name')
        password=request.form.get('password')
        user=User.query.filter_by(email=uname,password=password).first()
        if user and user.role==0:
            return redirect(url_for('admin_dashboard',name=user.full_name))
        elif user and user.role==1:
            return redirect(url_for("user_dashboard",name=user.full_name,id=user.id))
        else:
            return render_template('login.html', msg='invalid user')
    return render_template("login.html", msg="")
        
@app.route("/admin_dashboard/<name>")
def admin_dashboard(name):
    subjects=Subject.query.all()
    return render_template("admin_dashboard.html", name=name, subjects=subjects)

@app.route("/new_subject/<name>" ,methods=["GET","POST"])
def new_subject(name):
    if request.method=="POST":
        new_subject=request.form.get("new_subject")
        desc=request.form.get('desc')
        subject=Subject(name=new_subject,description=desc)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_dashboard',name=name))
    return render_template("newsubject.html", name=name)

@app.route("/new_chapter/<subject_id>/<name>" ,methods=["GET","POST"])
def new_chapter(subject_id,name):
    if request.method=="POST":
        new_chapter=request.form.get('newchapter')
        desc=request.form.get('description')
        chapter=Chapter(name=new_chapter,description=desc,subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for('admin_dashboard',name=name, msg="chapter added successfully" ))
    return render_template("newchapter.html", msg='',name=name)

@app.route("/new_chapter/<chapter_id>/<name>" ,methods=["GET","POST"])
def edit_chapter(chapter_id,name):
    chr=Chapter.query.filter_by(chapter_id)
    if request.method=="POST":
        chr_name=request.form.get("new_chapter")
        desc=request.form.get("desc")
        chr.name=chr_name
        chr.description=desc
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name, msg="updated successfully"))
    return render_template('subject_edit.html',msg="now you can edit",name=name, chr=chr)


@app.route("/subject/<subject_id>/<name>" ,methods=["GET","POST"])
def edit_subject(subject_id,name):
    subject=Subject.query.filter_by(subject_id)
    if request.method=="POST":
        sub_name=request.form.get("name")
        desc=request.form.get("desc")
        chr.name=sub_name
        chr.description=desc
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name, msg="updated successfully"))
    return render_template('subject_edit.html',msg="now you can edit",name=name, subject=subject)


@app.route("/new_chapter/<chapter_id>/delete" ,methods=["GET","POST"])
def delete_chapter(chapter_id,name):
    chapter=Chapter.query.filter_by(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return render_template("admin_dashboard.html", msg="", name=name)


@app.route("/new_question/<quiz_id>/<name>" ,methods=["GET","POST"])
def new_question(quiz_id,name):
    if request.method=="POST":
        qtit=request.form.get('title')
        qes=request.form.get('statement')
        o1=request.form.get('o1')
        o2=request.form.get("o2")
        o3=request.form.get("o3")
        o4=request.form.get("o4")
        ans=request.form.get("ans")
        question=Question(title=qtit,question=qes,option1=o1, option2=o2,option3=o3,option4=o4,answer=ans, Quiz_id=quiz_id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name,msg="question added successfully" ))

    return render_template("newquestion.html", quiz_id=quiz_id, name=name)

@app.route("/new_quiz/<name>" ,methods=["GET","POST"])
def new_quiz(name):
    chapter=Chapter.query.all()
    if request.method=="POST":
        chapter_id=request.form.get("chapter_id")
        date=request.form.get("datetime")
        T_score=request.form.get("total_score")
        duration=request.form.get("duration")
        d=datetime.fromisoformat(date)
        quiz=Quiz(Chapter_id=chapter_id,date=d,score=T_score,time_duration=duration)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("quiz_management", name=name, msg="quiz added"))
    return render_template("newquiz.html",chapter=chapter, name=name, msg="")

@app.route("/quiz_management/<name>" ,methods=["GET","POST"])
def quiz_management(name):
    quizzes=Quiz.query.all()
    return render_template("quiz_management.html", name=name,quizzes=quizzes)

@app.route("/user_dashboard/<name>/<id>" ,methods=["GET","POST"])
def user_dashboard(name,id):
    quizzes=Quiz.query.all()
    datetime_now=datetime.today().strftime('%Y-%m-%dT%H:%M')
    datetime_now=datetime.strptime(datetime_now,'%Y-%m-%dT%H:%M')
    return render_template("user_dashboard.html",name=name, id=id,quizzes=quizzes,datetime_now=datetime_now)

@app.route("/start_quiz/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def start_quiz(id,name,quiz_id):
    return render_template("startquiz.html",id=id,name=name,quiz_id=quiz_id)


@app.route("/view_quiz/<quiz_id>" ,methods=["GET","POST"])
def view_score(quiz_id):
    quiz=Quiz.query.filter_by(quiz_id)
    return render_template("view.html",quiz=quiz)

@app.route("/user_score/<name>/<id>" ,methods=["GET","POST"])
def scores(name,id):
    scores=Score.query.filter_by(id=id,name=name)
    return render_template("scores.html", name=name, scores=scores)


@app.route("/search/<name>" ,methods=["GET","POST"])
def admin_search(name):
    if request.method=="POST":
        search_txt=request.form.get("admin_search")
        by_user=User.query.filter(User.full_name.ilike(f"%{search_txt}")).all()
        by_subject=Subject.query.filter(Subject.name.ilike(f"%{search_txt}")).all()
        by_quiz=Quiz.query.filter(Quiz.name.ilike(f"%{search_txt}")).all()
        if by_user:
            render_template("admin_dashboard.html",name=name,users=by_user)
        elif by_subject:
            render_template("admin_dashboard.html",name=name,subjects=by_subject)
        elif by_quiz:
            render_template("admin_dashboard.html",name=name,quizzes=by_quiz)
    return redirect(url_for("admin_dashboard", name=name))


@app.route("/user_search/<name>" ,methods=["GET","POST"])
def user_search(name):
    if request.method=="POST":
        search_txt=request.form.get("admin_search")
        by_user=User.query.filter(User.name.ilike(f"%{search_txt}")).all()
        by_subject=Subject.query.filter(Subject.name.ilike(f"%{search_txt}")).all()
        by_quiz=Quiz.query.filter(Quiz.name.ilike(f"%{search_txt}")).all()
        if by_user:
            render_template("admin_dashboard.html",name=name,users=by_user)
        elif by_subject:
            render_template("admin_dashboard.html",name=name,subjects=by_subject)
        elif by_quiz:
            render_template("admin_dashboard.html",name=name,quizzes=by_quiz)
    return redirect(url_for("user_dashboard", name=name))


@app.route("/user_summary/<id>/<name>" ,methods=["GET","POST"])
def user_summary(id,name):
    return render_template("user_summary.html",id=id,name=name)

@app.route("/admin_summary/<name>" ,methods=["GET","POST"])
def admin_summary(name):
    return render_template("admin_summary.html", name=name)




    

if __name__=="__main__":
    app.run(debug=True)
