# endpoints/auth.py
from flask import Blueprint
from api.models import User

bp = Blueprint('auth', __name__, url_prefix="/auth")
