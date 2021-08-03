from flask import jsonify, make_response
from flask_restx import cors
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_cors import cross_origin
from api.v1 import api
from api.group_arguments import new_group_argument, room_argument
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.Group import Group
from api.models.User import User
import time

groups_ns = api.namespace('groups',description='Manages the groups created by users',decorators=[cors.crossdomain(origin="*")])

@groups_ns.route('/members/<groupID>',methods=['OPTIONS','GET'])
class GroupMembers(Resource):
	@cross_origin()
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self,groupID):
		"""
		Gets members of a given groups
		"""
		try:
			if groupID is not None:
				try:
					members = Group.getMembersOf(groupID)
					if(len(members) != 0):
						return make_response(jsonify(members),200)
					else:
						return make_response(jsonify("None"),404)
				except:
					return handle500error(groups_ns)
			else:
				raise Exception()
		except:
			return handle500error(groups_ns)

@groups_ns.route('/<username>',methods=['OPTIONS','DELETE','GET','POST'])

class UserGroups(Resource):
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
		Gets a user's work groups
		"""
		try:
			if username is not None and User.exists(username):
				groups = Group.getWorkGroups(username)
				if(len(groups) > 0):
					return make_response(jsonify(groups),200)
				else:
					return make_response(jsonify("No groups assigned to this user"),409)
			else:	
				raise Exception('Something went wrong with deletion')			
		except:
			handle400error(groups_ns,'Invalid username')		
		return handle500error(groups_ns)

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
		Deletes a group
		"""
		groupID = username #lazy
		try:
			returnValue = Group.delete(groupID)
			if returnValue:
				make_response(jsonify("Deleted"),200)	
		except:
			handle400error(groups_ns,'Invalid username')		
		return handle500error(groups_ns)

	@cross_origin()
	@limiter.limit('1000/hour')
	@api.expect(room_argument)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self,username):
		"""
		Assigns a room to the group
		"""
		args = room_argument.parse_args()
		room = args['roomID']
		group = args['groupID']
		try:
			returnValue = Group.assign(room,group)
			if returnValue:
				make_response(jsonify("Deleted"),200)	
		except:
			handle400error(groups_ns,'Invalid username')		
		return handle500error(groups_ns)

@groups_ns.route('',methods=['OPTIONS','POST'])

class Groups(Resource):
	@cross_origin()
	@limiter.limit('1000/hour')
	@api.expect(new_group_argument)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self):
		"""
		Creates a new group
		"""
		try:
			args = new_group_argument.parse_args()
			username = args.groupLeader
			userID = User.fetchByUsername(username)[0]
			groupName = args['name']
			path = args.path
			department = args.department
			try:
				group = Group(userID,groupName,path,department)
				returnedValue = group.insertNewGroup(username)
				if(not returnedValue):
					return make_response(jsonify("Created"),200)
				else:
					return make_response(jsonify("No groups assigned to this user"),409)
			except:
				return handle500error(groups_ns)
		except:
			return handle500error(groups_ns)