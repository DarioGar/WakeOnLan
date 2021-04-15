from api.config import POSTGRES_PASSWORD
from api.config import POSTGRES_USER
from api.config import POSTGRES_DB_NAME
from api.config import POSTGRES_PORT
from api.config import HOST

from flask_restx import Api
import psycopg2 as psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs


api = Api(version='1.0',
        title = 'Users API',
        description='')
con = psycopg2.connect(database= POSTGRES_DB_NAME,user=POSTGRES_USER,password=POSTGRES_PASSWORD,host=HOST,port=POSTGRES_PORT)
print(con)