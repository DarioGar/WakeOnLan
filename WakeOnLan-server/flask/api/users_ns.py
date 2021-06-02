import api.reusable
from flask_restx import Resource
from flask import jsonify, make_response
from flask_restx import cors
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import jwt_required
from api.user_arguments import user_args_name_arguments, new_user_arguments, user_delete_arguments
from api.reusable import get_hashed_password
from api.v1 import api
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.User import User

users_ns = api.namespace('users',description='Manages user information',decorators=[cors.crossdomain(origin="*")])

@users_ns.route('/signup',methods=['POST','OPTIONS'])
class userSignup(Resource):

	@cross_origin()
	@limiter.limit('1000/hour')
	@api.expect(new_user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
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
			email = args['email']
			if username and pw and fullname and role and email:
				alreadyInUse = User.exists(username)
			else:
				raise Exception("Provided arguments are not correct")
		except:
			return handle400error(users_ns,"The provided arguments are not correct. Please, check the swagger documentation at /v1")
		if alreadyInUse != (0,):
			return handle400error(users_ns,"The username is already in use")
		# Build the user
		try:
			user = User(username,get_hashed_password(pw),fullname,email)
			user.roles.append(role.lower())
			id = user.register()
			user.setRoles(role.lower())
			access_token = create_access_token(identity=id)
			response = jsonify(access_token)
			return make_response(response, 201)
		except:
			return handle500error(users_ns)

@users_ns.route('/login',methods=['POST','OPTIONS'])
class userCollection(Resource):
	@cross_origin()
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
			username = args.username
			pw = args.password
			
			data = User.authenticate(username,pw)
			if(data==None):
				raise Exception()
		except:
			return handle400error(users_ns, 'Invalid username and password combination')
		try:
			user = User(data[2],data[3],data[1],data[6])
			user.setRoles(data[4])
			if data:
				access_token=create_access_token(identity=user.__dict__)
				responseData = user.__dict__
				responseData['accessToken'] = access_token
				response = jsonify(responseData)
				return make_response(response, 200)
		except:
			return handle500error(users_ns)

@users_ns.route('/user',methods=['GET','OPTIONS'])

class user(Resource):

	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self):
		"""
		Gets all users
		"""
		try:
			responseData = User.fetchAll()
			if(len(responseData) > 0):
				response = jsonify(responseData)
			else:	
				response = jsonify()
			return make_response(response, 200)
		except:
			handle400error(users_ns,'Invalid username')
		
		return handle500error(users_ns)

@users_ns.route('/<username>',methods=['DELETE','OPTIONS'])

class user(Resource):
	cross_origin()
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def delete(self,username):
		"""
		Deletes a user
		"""
		try:
			if username is not None and User.exists(username):
				User.delete(username)
				return make_response(jsonify("Succesfully deleted" + username),200)
			else:	
				raise Exception('Something went wrong with deletion')			
		except:
			handle400error(users_ns,'Invalid username')
		
		return handle500error(users_ns)