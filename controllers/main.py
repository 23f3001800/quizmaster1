from flask import Flask, render_template,url_for, redirect,request
from flask import current_app as app
from models.database import db, Users, Subjects,Chapters, Questions, Quizzes, Scores
from datetime import datetime
import matplotlib.pyplot as plt


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
        user=Users.query.filter_by(email=uname).first()
        new_user=Users(full_name=fname,email=uname,password=password, qualification=quali,dob=dob)
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
        user=Users.query.filter_by(email=uname,password=password).first()
        if user and user.role==0:
            return redirect(url_for('admin_dashboard',name=user.full_name))
        elif user and user.role==1:
            return redirect(url_for("user_dashboard",name=user.full_name,id=user.id))
        else:
            return render_template('login.html', msg='invalid user')
    return render_template("login.html", msg="")
        
@app.route("/admin_dashboard/<name>")
def admin_dashboard(name):
    subjects=Subjects.query.all()
    return render_template("admin_dashboard.html", name=name, subjects=subjects)

@app.route("/new_subject/<name>" ,methods=["GET","POST"])
def new_subject(name):
    if request.method=="POST":
        new_subject=request.form.get("new_subject")
        desc=request.form.get('desc')
        subject=Subjects(name=new_subject,description=desc)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_dashboard',name=name))
    return render_template("newsubject.html", name=name)

@app.route("/subject/<subject_id>/<name>" ,methods=["GET","POST"])
def edit_subject(subject_id,name):
    subject=Subjects.query.filter_by(id=subject_id).first()
    if request.method=="POST":
        sub_name=request.form.get("new_subject")
        desc=request.form.get("desc")
        subject.name=sub_name
        subject.description=desc
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name, msg="updated successfully"))
    return render_template('subject_edit.html',msg="now you can edit",name=name, subject=subject)


@app.route("/subject/<subject_id>/<name>/delete" ,methods=["GET","POST"])
def delete_subject(subject_id,name):
    subject=Subjects.query.filter_by(id=subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for("admin_dashboard", msg="", name=name))

@app.route("/new_chapter/<subject_id>/<name>" ,methods=["GET","POST"])
def new_chapter(subject_id,name):
    if request.method=="POST":
        new_chapter=request.form.get('newchapter')
        desc=request.form.get('description')
        chapter=Chapters(name=new_chapter,description=desc,subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for('admin_dashboard',name=name, msg="chapter added successfully" ))
    return render_template("newchapter.html", msg='',name=name)

@app.route("/edit/<subject_id>/<chapter_id>/<name>" ,methods=["GET","POST"])
def edit_chapter(subject_id,chapter_id,name):
    chr=Chapters.query.filter_by(id=chapter_id).first()
    if request.method=="POST":
        chr_name=request.form.get("new_chapter")
        desc=request.form.get("desc")
        chr.name=chr_name
        chr.description=desc
        chr.subject_id=subject_id
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name, msg="updated successfully"))
    return render_template('edit_chapter.html',msg="now you can edit",name=name, chr=chr)

@app.route("/chapter/<chapter_id>/<name>/delete" ,methods=["GET","POST"])
def delete_chapter(chapter_id,name):
    chapter=Chapters.query.filter_by(id=chapter_id).first()
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for("admin_dashboard", msg="", name=name))

@app.route("/quiz_management/<name>" ,methods=["GET","POST"])
def quiz_management(name):
    quizzes=Quizzes.query.all()
    return render_template("quiz_management.html", name=name,quizzes=quizzes)

@app.route("/new_quiz/<name>" ,methods=["GET","POST"])
def new_quiz(name):
    chapter=Chapters.query.all()
    if request.method=="POST":
        chapter_id=request.form.get("chapter_id")
        date=request.form.get("datetime")
        score=request.form.get("total_score")
        duration=request.form.get("duration")
        d=datetime.fromisoformat(date)
        quiz=Quizzes(Chapter_id=chapter_id,date=d,score=score,time_duration=duration)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("quiz_management", name=name, msg="quiz added"))
    return render_template("newquiz.html",chapter=chapter, name=name, msg="")

@app.route("/edit_quiz/<quiz_id>/<name>" ,methods=["GET","POST"])
def edit_quiz(quiz_id,name):
    q=Quizzes.query.filter_by(id=quiz_id).first()
    if request.method=="POST":
        date=request.form.get("datetime")
        score=request.form.get("total_score")
        duration=request.form.get("duration")
        d=datetime.fromisoformat(date)
        q.date=d
        q.score=score
        q.duration=duration
        db.session.commit()
        return redirect(url_for("quiz_management", name=name, msg="updated successfully"))
    return render_template('edit_quiz.html',msg="now you can edit",name=name, q=q)


@app.route("/quiz/<quiz_id>/<name>/delete" ,methods=["GET","POST"])
def delete_quiz(quiz_id,name):
    q=Quizzes.query.filter_by(id=quiz_id).first()
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin_dashboard.html", msg="", name=name))

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
        question=Questions(title=qtit,question=qes,option1=o1, option2=o2,option3=o3,option4=o4,answer=ans, Quiz_id=quiz_id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("new_question", quiz_id=quiz_id, name=name))
    q_count=Questions.query.filter_by(Quiz_id=quiz_id).count()
    return render_template("newquestion.html", quiz_id=quiz_id, name=name, q_count=q_count)


@app.route("/edit_question/<question_id>/<name>" ,methods=["GET","POST"])
def edit_question(question_id,name):
    q=Questions.query.filter_by(id=question_id).first()
    if request.method=="POST":
        qtit=request.form.get('title')
        ques=request.form.get('statement')
        o1=request.form.get('o1')
        o2=request.form.get("o2")
        o3=request.form.get("o3")
        o4=request.form.get("o4")
        ans=request.form.get("ans")
        db.session.commit()
        q.title=qtit
        q.question=ques
        q.option1=o1
        q.option=o2
        q.option=o3
        q.option=o4
        q.answer=ans
        db.session.commit()
        return redirect(url_for("quiz_management", name=name, msg="updated successfully"))
    return render_template('edit_question.html',msg="now you can edit",name=name, q=q)

@app.route("/question/<question_id>/<name>/delete" ,methods=["GET","POST"])
def delete_question(question_id,name):
    q=Questions.query.filter_by(id=question_id).first()
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("quiz_management", msg="", name=name))


@app.route("/users/<name>" ,methods=["GET","POST"])
def user_dashboard(name):
    users=Users.query.all()
    return render_template("users.html",name=name, users=users)


@app.route("/user_dashboard/<id>/<name>" ,methods=["GET","POST"])
def user_dashboard(name,id):
    quizzes=Quizzes.query.all()
    datetime_now=datetime.today().strftime('%Y-%m-%dT%H:%M')
    datetime_now=datetime.strptime(datetime_now,'%Y-%m-%dT%H:%M')
    return render_template("user_dashboard.html",name=name, id=id, quizzes=quizzes, datetime_now=datetime_now)

@app.route("/start_quiz/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def start_quiz(id,name,quiz_id):
    quiz=Quizzes.query.filter_by(id=quiz_id).first()
    qu=quiz.Question
    index=0
    if index>=len(qu):
        return redirect(url_for("result",quiz_id=quiz_id))
    tscore=0
    q=qu[index]
    if request.method=="POST":
        user_ans=request.form.get("answer")
        if user_ans==q.answer:
            tscore=tscore+q.marks
        else:
            tscore=tscore
        return redirect(url_for("start_quiz", id=id,name=name,q=q,index=index+1))
    scores=Scores(Quiz_id=quiz_id,user_id=id,score=tscore,)
    return render_template("startquiz.html",id=id,name=name,quiz=quiz)


@app.route("/view_quiz/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def view_score(id,name,quiz_id):
    quiz=Quizzes.query.filter_by(quiz_id)
    return render_template("view.html",quiz=quiz,id=id,name=name)

@app.route("/view_quiz_d/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def view_quiz_details(id,quiz_id,name):
    quiz=Quizzes.query.filter_by(id=quiz_id).first()
    return render_template("view_quiz_details.html",quiz=quiz,name=name,id=id)

@app.route("/user_score/<id>/<name>" ,methods=["GET","POST"])
def scores(id,name):
    scores=Scores.query.filter_by(user_id=id)
    return render_template("scores.html",id=id, name=name, scores=scores)


@app.route("/search/<name>" ,methods=["GET","POST"])
def admin_search(name):
    if request.method=="POST":
        search_txt=request.form.get("admin_search")
        by_user=Users.query.filter(Users.full_name.ilike(f"%{search_txt}")).all()
        by_score=Subjects.query.filter(Scores.date.ilike(f"%{search_txt}")).all()
        by_quiz=Quizzes.query.filter(Quizzes.name.ilike(f"%{search_txt}")).all()
        if by_user:
           render_template("users.html",name=name,users=by_user)
        if by_score:
            render_template("score.html",name=name,score=by_score)
        elif by_quiz:
            render_template("quiz_management.html",name=name,quizzes=by_quiz)
        
    return redirect(url_for("admin_dashboard", name=name))


@app.route("/user_search/<name>" ,methods=["GET","POST"])
def user_search(name):
    if request.method=="POST":
        search_txt=request.form.get("admin_search")
        #by_user=Users.query.filter(Users.name.ilike(f"%{search_txt}")).all()
        by_subject=Subjects.query.filter(Subjects.name.ilike(f"%{search_txt}")).all()
        by_quiz=Quizzes.query.filter(Quizzes.name.ilike(f"%{search_txt}")).all()
        #if by_user:
         #   render_template("admin_dashboard.html",name=name,users=by_user)
        if by_subject:
            render_template("admin_dashboard.html",name=name,subjects=by_subject)
        elif by_quiz:
            render_template("admin_dashboard.html",name=name,quizzes=by_quiz)
    return redirect(url_for("user_dashboard", name=name))


@app.route("/user_summary/<id>/<name>" ,methods=["GET","POST"])
def user_summary(id,name):
    plt=get_plt()
    plt.savefig("./static/images/admin_summary.jpeg")
    plt.clf()

    return render_template("user_summary.html",id=id,name=name)

@app.route("/admin_summary/<name>" ,methods=["GET","POST"])
def admin_summary(name):
    plt=get_plt()
    plt.savefig("./static/images/admin_summary.jpeg")
    plt.clf()
    return render_template("admin_summary.html", name=name)

def get_plt():
    sub=Subjects.query.all()
    l={}
    for s in sub:
        l[s.name]=s.chapter.quiz.score
    x_label=list(l.keys())
    y_lable=list(l.values())
    plt.bar(x_label,y_lable,color="red",width=.4)
    plt.title('subject vs score')
    plt.xlabel('sub')
    plt.ylabel('score')
    return plt




    

if __name__=="__main__":
    app.run(debug=True)
