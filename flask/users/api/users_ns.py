import api.reusable
import base64
import bcrypt
import json
from markupsafe import escape
from flask_restx import Resource
from api.user_arguments import user_args_name_arguments, user_arguments
from api.user_models import user_model
from api.v1 import api
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.reusable import check_password,get_hashed_password,checkMAC
from api.v1 import db
from bson import ObjectId


users_ns = api.namespace('users',description='Manages user information')

@users_ns.route('/signup')
class userSignup(Resource):

	@limiter.limit('1000/hour')
	@api.expect(user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def post(self):
		"""
		Creates a user
		"""
		try:
			args = user_arguments.parse_args()
			username = args['username']
			pw = args['information']['password']
			users = list(db.users.find({},{"_id" : 0 ,"username" : 1}))
			# Check if the username is already in use
			# We create a list of only the username field from the list of dictionaries returned from db.users.find()
			if username not in [d['username'] for d in users]:
				# Hash and salt the password before storing it
				hash_pw = get_hashed_password(pw)
				user_id = db.users.insert_one({"username" : username, "password" : hash_pw}).inserted_id
				return str(user_id)
		except:
			handle500error(users_ns)
		handle400error(users_ns,"The username is already in use")

@users_ns.route('/login')
class userCollection(Resource):


	@limiter.limit('1000/hour')
	@api.expect(user_args_name_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@api.marshal_with(user_model, code=200, description='OK', as_list=True)

	def get(self):
		"""
		Returns a user's logged information, if the given user exists
		"""
		# Retrieve and check arguments
		try:
			args = user_args_name_arguments.parse_args()
			# Comprobar si existe el usuario y la contraseña en la base de datos
			username = args['username']
			pw = args['password']
			if username is not None and pw is not None:
				users = list(db.users.find({},{"_id" : 0}))
				# Check if the username is already in use
				# We create a list of only the username field from the list of dictionaries returned from db.users.find()
				for user in users:
					if username == user["username"]:
						if check_password(pw,user['password']):
							# Logged in
							return {'name' : username}
			raise Exception('Invalid username and password combination')
		except:
			return handle400error(users_ns, 'Invalid username and password combination')

		return handle500error(users_ns)

@users_ns.route('/user')
class userDelete(Resource):

	@limiter.limit('1000/hour')
	@api.expect(user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def delete(self):
		"""
		Deletes a user
		"""
		try:
			args = user_arguments.parse_args()
			username = args['username']
			pw = args['information']['password']
			if username is not None and pw is not None:
				users = list(db.users.find({}))
				for user in users:
					if username == user['username']:
						if check_password(pw,user['password']):
							# Delete de user
							print("Usuario eliminado")
							db.users.delete_one({"username" : user['username']})
							return str(user["_id"])
							
			raise Exception('Invalid username and password combination')
					
		except:
			handle404error(users_ns,'Invalid username and password combination')
			
		return handle500error(users_ns)


