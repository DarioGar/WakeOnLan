import api.reusable
import base64
import bcrypt
import json
from markupsafe import escape
from flask_restx import Resource
from api.user_arguments import user_args_name_arguments, user_arguments
from api.user_models import user_model
from api.v1 import api,con
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.reusable import check_password,get_hashed_password,checkMAC
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
		#Retrieve arguments
		try:
			args = user_arguments.parse_args()
			username = args['username']
			pw = args['password']
			fullname =args['fullname']
			role = args['role']
			cur = con.cursor()
			if username is not None:
				query = "select count(1) from public.users where username = %s"
				cur.execute(query,(username,))
				rows = cur.fetchall()
				print(rows[0])
		except:
			return handle400error(users_ns,"The provided arguments are not correct. Please, check the swagger documentation at /v1")
		if rows[0] != (0,):
			return handle400error(users_ns,"The username is already in use")
		# Build the user
		try:
			cur = con.cursor()
			# Hash and salt the password before storing it
			hash_pw = get_hashed_password(pw)
			query = "INSERT INTO public.users (full_name,username,password,role) VALUES (%s,%s,%s,%s)"
			cur.execute(query,(fullname,username,hash_pw,role))
			con.commit()
			return "success"
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
class user(Resource):

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

	@limiter.limit('1000/hour')
	@api.expect(user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def get(self):
		"""
		Deletes a user
		"""
		try:
			args = user_arguments.parse_args()
			username = args['username']
			pw = args['password']
			if username is not None and pw is not None:
				
				for user in users:
					if username == user['username']:
						if check_password(pw,user['password']):
							# Delete de user
							print("Usuario eliminado")

							return str(user["_id"])
							
			raise Exception('Invalid username and password combination')
					
		except:
			handle404error(users_ns,'Invalid username and password combination')
			
		return handle500error(users_ns)


