import api.reusable
import base64
import bcrypt
from markupsafe import escape
from flask_restx import Resource
from api.user_arguments import user_args_name_arguments, user_arguments,mac_arguments
from api.user_models import user_model
from api.v1 import api
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.reusable import check_password,get_hashed_password,checkMAC

users_ns = api.namespace('users',description='Manages user information')
usuarios = [{'username' : 'John','password' : 'X2B43uz+GaOhuaN1OkTdvA=='}]

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
			for user in usuarios:
				# Check if the username is already in use
				if username not in user.values():
					# Hash and salt the password before storing it
					hash_pw = base64.b64encode(get_hashed_password(pw))
					new_user = {"username" : username, "password" : hash_pw.decode('ascii')}
					# Insert into either Mongo or Postgre
					usuarios.append(new_user)
					return new_user
		except:
			handle500error(users_ns)

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
				for user in usuarios:
					if username in user.values():
						if check_password(pw,base64.b64decode(user['password'])):
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
				for index, user in enumerate(usuarios):
					if username in user.values():
						if check_password(pw,base64.b64decode(user['password'])):
							# Delete de user
							print("Usuario eliminado")
							usuarios.remove(user)
							return "Eliminado"
							
			raise Exception('Invalid username and password combination')
					
		except:
			handle404error(users_ns,'Invalid username and password combination')
			
		return handle500error(users_ns)


