from flask import Flask, render_template,url_for, redirect,request
from flask import current_app as app
from models.database import db, Users, Subjects,Chapters, Questions, Quizzes, Scores
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sqlalchemy import text


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
            if user.status=="Blocked":
                return render_template('login.html',msg="you are blocked by admin kindly contact this mail admin@gmail.com")
            return redirect(url_for("user_dashboard",name=user.full_name,id=user.id))
        else:
            return render_template('login.html', msg='invalid user')
    return render_template("login.html", msg="login here")
        
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
        return redirect(url_for('admin_dashboard',name=name,msg="suject added successfully"))
    return render_template("newsubject.html", name=name,msg="add subject here")

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
        title=request.form.get("title")
        date=request.form.get("datetime")
        score=request.form.get("total_score")
        duration=request.form.get("duration")
        d=datetime.fromisoformat(date)
        quiz=Quizzes(Chapter_id=chapter_id,date=d,title=title,total_score=score,time_duration=duration)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("quiz_management", name=name, msg="quiz added"))
    return render_template("newquiz.html",chapter=chapter, name=name, msg="")

app.route("/view_quiz_detail/<name>/<quiz_id>" ,methods=["GET","POST"])
def admin_quiz_details(quiz_id,name):
    quiz=Quizzes.query.filter_by(id=quiz_id).first()
    return render_template("adminview_quiz_d.html",quiz=quiz,name=name)

@app.route("/edit_quiz/<quiz_id>/<name>" ,methods=["GET","POST"])
def edit_quiz(quiz_id,name):
    q=Quizzes.query.filter_by(id=quiz_id).first()
    if request.method=="POST":
        date=request.form.get("datetime")
        score=request.form.get("total_score")
        duration=request.form.get("duration")
        d=datetime.fromisoformat(date)
        q.date=d
        q.total_score=score
        q.duration=duration
        db.session.commit()
        return redirect(url_for("quiz_management", name=name, msg="updated successfully"))
    return render_template('edit_quiz.html',msg="now you can edit",name=name, q=q)


@app.route("/quiz/<quiz_id>/<name>/delete" ,methods=["GET","POST"])
def delete_quiz(quiz_id,name):
    q=Quizzes.query.filter_by(id=quiz_id).first()
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("quiz_management", msg="deleted successfuly", name=name))

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
        ques=request.form.get('statement')
        o1=request.form.get('o1')
        o2=request.form.get("o2")
        o3=request.form.get("o3")
        o4=request.form.get("o4")
        ans=request.form.get("ans")
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
    return redirect(url_for("quiz_management", msg="deleted successfuly", name=name))


@app.route("/users/<name>" ,methods=["GET","POST"])
def users(name):
    users=Users.query.filter_by(role=1).all()
    return render_template("users.html",name=name, users=users)


@app.route("/block/<user_id>/<name>" ,methods=["GET","POST"])
def block(name,user_id):
    user=Users.query.filter_by(id=user_id).first()
    user.status="Blocked"
    db.session.commit()
    return redirect(url_for("users",name=name,msg="user blocked successfully"))

@app.route("/unblock/<user_id>/<name>" ,methods=["GET","POST"])
def unblock(name,user_id):
    user=Users.query.filter_by(id=user_id).first()
    user.status="Active"
    db.session.commit()
    return redirect(url_for("users",name=name,msg="user blocked successfully"))


@app.route("/user_dashboard/<id>/<name>" ,methods=["GET","POST"])
def user_dashboard(name,id):
    quizzes=Quizzes.query.all()
    datetime_now=datetime.today().strftime('%Y-%m-%dT%H:%M')
    datetime_now=datetime.strptime(datetime_now,'%Y-%m-%dT%H:%M')
    return render_template("user_dashboard.html",name=name, id=id, quizzes=quizzes, datetime_now=datetime_now)

@app.route("/start_quiz/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def start_quiz(id,name,quiz_id):
    quiz=Quizzes.query.filter_by(id=quiz_id).first()
    if datetime.now() < quiz.date:
        return "quiz is not started yet"
    ques=Questions.query.filter_by(Quiz_id=quiz_id).all()
    total=len(ques)
    scores=Scores.query.filter_by(user_id=id,Quiz_id=quiz_id).first()
    attempt=0
    if not scores:
        scores=Scores(user_id=id,Quiz_id=quiz_id,score=0,date=quiz.date)
        db.session.add(scores)
        db.session.commit()

    if request.method=="POST":
        q_id=request.form.get("q_id",type=int)
        ans=request.form.get("answer",type=int)
        print(ans)
        q_index=request.form.get("q_index",type=int)
        action=request.form.get("action")
        question=Questions.query.filter_by(id=q_id).first()
        print(question.answer)
        next_index=q_index+1
        #if ans==int(question.answer):
        #### else:
        #next_index=0
    #current_question=ques[next_index]
        if action=="save":
            if ans:
                if ans==int(question.answer):
                    scores.score+=10
                    attempt+=1
                    db.session.commit()
                else:
                    attempt+=1
                    scores.score+=0
                    db.session.commit()
        if action=="submit" or next_index>=total:
            return redirect(url_for('view_result', id=id,quiz_id=quiz_id,name=name))

    else:
        next_index=0  
    current_question=ques[next_index]
    quiz.status="Closed"
    db.session.commit()
    return render_template("startquiz.html",name=name,id=id,quiz_id=quiz_id,question=current_question,q_index=next_index,total=total)


@app.route("/view_quiz/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def view_result(id,name,quiz_id):
    quiz=Quizzes.query.filter_by(id=quiz_id).first()
    scores=Scores.query.filter_by(user_id=id,Quiz_id=quiz_id).first()
    correct=scores.score//10
    total_q=Questions.query.filter_by(Quiz_id=quiz_id).count()
    return render_template("view_result.html",your_score=scores,id=id,total=total_q,name=name, quiz=quiz,correct=correct)

@app.route("/view_quiz_d/<id>/<name>/<quiz_id>" ,methods=["GET","POST"])
def view_quiz_details(id,quiz_id,name):
    quiz=Quizzes.query.filter_by(id=quiz_id).first()
    return render_template("view_quiz_details.html",quiz=quiz,name=name,id=id)

@app.route("/user_score/<id>/<name>" ,methods=["GET","POST"])
def scores(id,name):
    scores=Scores.query.filter_by(user_id=id)
    return render_template("scores.html",id=id, name=name,scores=scores)


@app.route("/search/<name>" ,methods=["GET","POST"])
def admin_search(name):
    if request.method=="POST":
        search_txt=request.form.get("admin_search")
        by_user=Users.query.filter(Users.full_name.ilike(f"%{search_txt}")).all()
        by_score=Subjects.query.filter(Scores.date.ilike(f"%{search_txt}")).all()
        by_quiz=Quizzes.query.filter(Quizzes.title.ilike(f"%{search_txt}")).all()
        if by_user:
           render_template("users.html",name=name,users=by_user)
        if by_score:
            render_template("score.html",name=name,score=by_score)
        elif by_quiz:
            render_template("quiz_management.html",name=name,quizzes=by_quiz)
        
    return redirect(url_for("admin_dashboard", name=name))


@app.route("/user_search/<name>/<id>" ,methods=["GET","POST"])
def user_search(name,id):
    if request.method=="POST":
        search_txt=request.form.get("admin_search")
        by_quiz=Quizzes.query.filter(Quizzes.title.ilike(f"%{search_txt}")).all()
        if by_quiz:
            render_template("user_dashboard.html",name=name,quizzes=by_quiz,id=id)
    return redirect(url_for("user_dashboard", name=name,id=id))


@app.route("/user_summary/<id>/<name>" ,methods=["GET","POST"])
def user_summary(id,name):
    get_user_plt(id).savefig("./static/images/user_summary1.jpeg")
    plt.clf()
    get_u_pie_plt(id).savefig("./static/images/user_summary2.jpeg")
    plt.close()

    return render_template("user_summary.html",id=id,name=name)

@app.route("/admin_summary/<name>" ,methods=["GET","POST"])
def admin_summary(name):
    get_plt().savefig("./static/images/admin_summary1.jpeg")
    plt.clf()
    get_pie_plt().savefig("./static/images/admin_summary2.jpeg")
    plt.clf()


    return render_template("admin_summary.html", name=name)

def get_plt():
    results=db.session.execute(text("""
    select Subjects.name ,max(Scores.score)
    from Subjects
    join Chapters on Subjects.id=Chapters.subject_id          
    join Quizzes on Chapters.id=Quizzes.chapter_id
    join Scores on Quizzes.id=Scores.Quiz_id
    group by Subjects.name                          
    """)).fetchall()
    l=dict(results)
    x_label=list(l.keys())
    y_lable=list(l.values())
    plt.bar(x_label,y_lable,color="red",width=.4)
    plt.title('subject vs score')
    plt.xlabel('sub')
    plt.ylabel('score')
    return plt

def get_user_plt(user_id):
    results=db.session.execute(text("""
    select Subjects.name ,count(Quizzes.id)
    from Subjects
    join Chapters on Subjects.id=Chapters.subject_id          
    join Quizzes on Chapters.id=Quizzes.chapter_id
    join Scores on Scores.Quiz_id=Quizzes.id
    where Scores.user_id=:user_id
    group by Subjects.name                          
    """),{"user_id":user_id}).fetchall()
    l=dict(results)
    x_label=list(l.keys())
    y_lable=list(l.values())
    plt.bar(x_label,y_lable,color="red",width=.4)
    plt.title('subject vs Quizzes')
    plt.xlabel('sub')
    plt.ylabel('Quizzes')
    return plt
def get_pie_plt():
    results=db.session.execute(text("""
    select Subjects.name ,count(Scores.id)
    from Subjects
    join Chapters on Subjects.id=Chapters.subject_id          
    join Quizzes on Chapters.id=Quizzes.chapter_id
    join Scores on Quizzes.id=Scores.Quiz_id
    join Users on Scores.user_id=Users.id
    group by Subjects.name                          
    """),{"user_id":id}).fetchall()
    l=dict(results)
    x_label=list(l.keys())
    y_label=list(l.values())
    plt.pie(y_label, labels=x_label)
    return plt

def get_u_pie_plt(user_id):
    results=db.session.execute(text("""
    select Subjects.name ,count(Scores.id)
    from Subjects
    join Chapters on Subjects.id=Chapters.subject_id          
    join Quizzes on Chapters.id=Quizzes.chapter_id
    join Scores on Scores.Quiz_id=Quizzes.id
    where Scores.user_id=:user_id
    group by Subjects.name                          
    """),{"user_id":user_id}).fetchall()
    l=dict(results)
    x_label=list(l.keys())
    y_label=list(l.values())
    plt.pie(y_label, labels=x_label)
    return plt



    

if __name__=="__main__":
    app.run(debug=True)
