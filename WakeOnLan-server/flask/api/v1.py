from flask_restx import Api
import psycopg2 as psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs

WOL_PASSWORD = "12345"
WOL_USER = "postgres"
WOL_DB_NAME = "wakeonlan"
WOL_PORT = 5432

api = Api(version='1.0',
        title = 'Users API',
        description='')

con = psycopg2.connect(dbname=WOL_DB_NAME,user=WOL_USER,password=WOL_PASSWORD)