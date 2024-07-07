from flask import Flask
from backend.database import db
app=None


def init_app():
    adviser_app=Flask(__name__)
    adviser_app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    adviser_app.debug=True
    adviser_app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///adviser_database.sqlite3"
    adviser_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(adviser_app)
    adviser_app.app_context().push()

    return adviser_app

app=init_app()

from backend.ads import *

if __name__=="__main__":
    app.run()