from flask import Flask, render_template,url_for, redirect
from flask import current_app as app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_up",methods=["GET","POST"])
def sign_up():
    return render_template("signup.html")

    

if __name__=="__main__":
    app.run(debug=True)
