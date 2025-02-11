from flask import Flask, render_template,url_for, redirect
from flask import current_app as app
import os

app=None

from controllers.main import *

def my_app():
    app=Flask(__name__)
    app.debug=True
    app.app_context().push()

if __name__=="__main__":
    app.run(debug=True)
