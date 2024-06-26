from flask import Flask
from backend.database import db
app=None

def init_app():
    adviser_app=Flask(__name__)
    adviser_app.debug=True
    adviser_app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///adviserdatabase.sqlite3"
    db.init_app(adviser_app)
    adviser_app.app_context().push()

    return adviser_app

app=init_app()

from backend.controllers import *

if __name__=="__main__":
    app.run()