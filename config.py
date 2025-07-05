import os

class Config:
    SECRET_KEY = 'sangat-rahasia'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/spk_saw_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
