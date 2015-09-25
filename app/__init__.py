from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#import os
#from flask.ext.login import LoginManager

#from flask.ext.moment import Moment
####
from flask.ext.bootstrap import Bootstrap
###

app = Flask(__name__)
app.config.from_object('config')
#moment = Moment(app)
db = SQLAlchemy(app)
#This is for AWS, delete the # when use
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sanilife:sanilife@sanidb.c2pz7qitscgg.us-west-2.rds.amazonaws.com:3306/sanidb'

# Uncomment the line below if you want to work with a local DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

 ######################################################################
from models import db
db.init_app(app)
with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.drop_all()
        db.create_all()
#######################


#lm = LoginManager()
#lm.init_app(app)
#lm.login_view = 'login'

###
bootstrap = Bootstrap(app)
###

from app import views, models
