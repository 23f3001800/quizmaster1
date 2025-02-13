from flask import Flask
from models.database import db


app=None


def my_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Quiz_mater.sqlite3"
    db.init_app(app)
    app.app_context().push()
    app.debug=True

my_app()

from controllers.main import *


if __name__=="__main__":
    app.run(debug=True)
