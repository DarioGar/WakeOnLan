import api.reusable
from flask_restx import Resource
from flask import jsonify, make_response
from flask_restx import cors
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import jwt_required
from api.arguments.user_arguments import user_args_name_arguments, new_user_arguments,invite_user_arguments,manage_invite_user_arguments,update_user_arguments
from api.reusable import get_hashed_password
from api.v1 import api
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.User import User

users_ns = api.namespace('users',description='Manages user information',decorators=[cors.crossdomain(origin="*")])

@users_ns.route('/signup',methods=['POST','OPTIONS'])
class UserSignup(Resource):

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
class UserLogin(Resource):
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
			# Comprobar si existe el usuario y la contrase??a en la base de datos
			username = args.username
			pw = args.password
			data = User.authenticate(username,pw)
			if(data==None):
				raise Exception()
		except:
			return handle400error(users_ns, 'Invalid username and password combination')
		try:
			user = User(data[2],data[3],data[1],data[6])
			user.setRoles(data[5])
			if data:
				access_token=create_access_token(identity=user.__dict__)
				responseData = user.__dict__
				responseData['accessToken'] = access_token
				response = jsonify(responseData)
				return make_response(response, 200)
		except:
			return handle500error(users_ns)

@users_ns.route('/user/<username>',methods=['GET','PUT','OPTIONS','DELETE'])

class UserCollection(Resource):

	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self,username):
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

	@limiter.limit('1000/hour')
	@api.expect(update_user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def put(self,username):
		"""
		Updates data and password of a user
		"""
		args = update_user_arguments.parse_args()
		username = args['username']
		pw = args['password']
		fullname =args['fullname']
		role = args['role']
		email = args['email']
		passwordChanged = args['pw']
		try:
			if(passwordChanged):
				result = User.updateUserDataAndPassword(username,get_hashed_password(pw),fullname,role,email)
				if(result==0):
					return make_response(jsonify("Updated " + username + "and password"),200)
			else:
				result = User.updateUserData(username,fullname,role,email)
				if(result==0):
					return make_response(jsonify("Updated " + username),200)
			return handle500error(users_ns)
		except:
			return handle500error(users_ns)

	@cross_origin()
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
				result = User.delete(username)
				return make_response(jsonify("Succesfully deleted" + username),200)
			else:	
				raise Exception('Something went wrong with deletion')			
		except:
			handle400error(users_ns,'Invalid username')
		
		return handle500error(users_ns)


@users_ns.route('/invites/',methods=['POST','OPTIONS'])
@users_ns.route('/invites/<username>',methods=['OPTIONS','GET','PUT'])

class Invites(Resource):
	cross_origin()
	@limiter.limit('1000/hour')
	@api.expect(invite_user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self):
		"""
		Sends an invitation to the user
		"""
		try:
			args = invite_user_arguments.parse_args()
			sender = args.sender
			to = args.to
			groupId = args.group
			try:
				if groupId is not None and User.exists(to):
					id = User.sendInvite(sender,to,groupId)
					if(id[0]!=-1):
						return make_response(jsonify(id[0],200))
					else:
						return make_response(jsonify("User has already been invited"),409)
				else:
					raise Exception()
			except:
				return handle400error(users_ns,'Invalid parameters')
		except:
			return handle500error(users_ns)

	@cross_origin()
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self,username):
		"""
		Gets invitations sent to the user passed as param
		"""

		if username is not None and User.exists(username):
			invitations = User.getInvitations(username)
			returnData = [[]]
			if(len(invitations) == 1):
				returnData = []
			if(len(invitations) > 1):
				returnData = [[]]
			if(len(invitations) != 0):
				for (index,i) in enumerate(invitations):
					if(i[4] == 'on hold'):
						returnData.append(list(i))
						returnData[index][1] = User.fetch(i[1])
				return make_response(jsonify(returnData),200)
			else:
				return make_response(jsonify("None"),404)



	@cross_origin()
	@limiter.limit('1000/hour')
	@api.expect(manage_invite_user_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def put(self,username):
		"""
		Accepts or refuses the invitation
		"""
		try:
			action = username
			args = manage_invite_user_arguments.parse_args()
			invitationID = args.id
			userID = args.userId
			groupID = args.groupId
			try:
				if action == 'accept' and (invitationID and userID and groupID):
					e = User.acceptInvitation(invitationID)
					if (e == 0):
						User.addUserToGroup(userID,groupID)
						return make_response(jsonify("Succesful"),200)
					else:
						return make_response(jsonify(e),500)
				elif action == 'deny' and invitationID:
					User.denyInvitation(invitationID)
				else:
					raise Exception()
			except:
				return handle500error(users_ns)
		except:
			return handle400error(users_ns,'Invalid parameters')


