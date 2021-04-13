from flask_restx import fields
from api.v1 import api

user_model = api.model('Information',{
    'name' : fields.String(example='John')
}, description='A user\'s login information')