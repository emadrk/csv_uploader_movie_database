import os

class Config:

    SQLALCHEMY_DATABASE_URI = 'postgresql://{userName}:{password}@{host}/{dbName}}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
