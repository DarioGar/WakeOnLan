from flask_restx import Api
from flask import Flask
import psycopg2 as psycopg2

WOL_PASSWORD = "12345"
WOL_USER = "postgres"
WOL_DB_NAME = "wakeonlan"
WOL_PORT = 5432
WOL_HOST = "192.168.0.20"


api = Api(version='1.0',
        title = 'Wake On Lan API',
        description='Manages all data to make the Wake On LAN web work')

con = psycopg2.connect(dbname=WOL_DB_NAME,user=WOL_USER,password=WOL_PASSWORD,host=WOL_HOST)
