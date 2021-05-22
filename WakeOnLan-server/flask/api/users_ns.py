import api.reusable
import base64
import json
from markupsafe import escape
from flask_restx import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import jwt_required
from api.user_arguments import user_args_name_arguments, new_user_arguments, user_delete_arguments
from api.user_models import user_model
from api.reusable import get_hashed_password
from api.v1 import api,con
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.User import User

users_ns = api.namespace('users',description='Manages user information')

@users_ns.route('/signup')
class userSignup(Resource):

	@limiter.limit('1000/hour')
	@api.expect(new_user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def post(self):
		"""
		Creates a user
		"""
		#Retrieve arguments
		try:
			args = new_user_arguments.parse_args()
			username = args['username']
			pw = args['password']
			fullname =args['fullname']
			role = args['role']
			if username is not None:
				alreadyInUse = User.get(username)
		except:
			return handle400error(users_ns,"The provided arguments are not correct. Please, check the swagger documentation at /v1")
		if alreadyInUse != (0,):
			return handle400error(users_ns,"The username is already in use")
		# Build the user
		try:
			user = User(username,get_hashed_password(pw),fullname,role)
			id = user.register()
			access_token = create_access_token(identity=id)
			refresh_token = create_refresh_token(identity=id)
			response = jsonify()
			set_access_cookies(response,access_token)
			set_refresh_cookies(response,refresh_token)
			return make_response(response, 201)
		except:
			return handle500error(users_ns)

@users_ns.route('/login')
class userCollection(Resource):


	@limiter.limit('1000/hour')
	@api.expect(user_args_name_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)

	def post(self):
		"""
		Returns a user's logged information, if the given user exists
		"""
		# Retrieve and check arguments
		try:
			args = user_args_name_arguments.parse_args()
			# Comprobar si existe el usuario y la contraseña en la base de datos
			username = args['username']
			pw = args['password']
			
			user = User.authenticate(username,pw)
			if user:
				access_token=create_access_token(user)
				refresh_token=create_refresh_token(user)
		
				response = jsonify()
				set_access_cookies(response, access_token)
				set_refresh_cookies(response, refresh_token)
				return make_response(response, 201)
			else:
				return handle400error(users_ns, 'Invalid username and password combination')
		except:
			return handle500error(users_ns)

@users_ns.route('/user')

class user(Resource):
	
	@limiter.limit('1000/hour')
	@api.expect(user_delete_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def delete(self):
		"""
		Deletes a user
		"""
		try:
			args = user_delete_arguments.parse_args()
			username = args['username']
			if username is not None:
				User.delete(username)
			else:	
				raise Exception('Something went wrong with deletion')			
		except:
			handle404error(users_ns,'Invalid username')
		
		return handle500error(users_ns)