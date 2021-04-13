
from flask_restx import Api
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wakeonlan

api = Api(version='1.0',
        title = 'Users API',
        description='')