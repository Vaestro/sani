import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sanilife:sanilife@sanidb.c2pz7qitscgg.us-west-2.rds.amazonaws.com:3306/sanidb'
# Uncomment the line below if you want to work with a local DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

CSRF_ENABLED = True
SECRET_KEY = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'
PUBLISHABLE_KEY = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'
