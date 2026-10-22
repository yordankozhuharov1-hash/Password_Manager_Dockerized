import os

class Config:
    SECRET_KEY ="change_this_later"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vault.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False