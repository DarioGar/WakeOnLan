from flask import jsonify, make_response
from flask_restx import cors
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_cors import cross_origin
from api.v1 import api
from api.models.Room import Room
from api.models.Computer import Computer
from api.room_arguments import room_computers_argument, new_room_argument
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error

rooms_ns = api.namespace('rooms',description='Manages the rooms in which the computers are located',decorators=[cors.crossdomain(origin="*")])


@rooms_ns.route('/room/',methods=['GET','POST','OPTIONS'])

class Rooms(Resource):
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def get(self):
		"""
		Returns all rooms
		"""
		try:
			rooms = Room.fetchAll()
		except:
			handle500error(rooms_ns)
		response = jsonify(rooms)
		return make_response(response,200)

	@limiter.limit('1000/hour')
	@api.expect(new_room_argument)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def post(self):
		"""
		Creates a room
		"""
		try:
			args = new_room_argument.parse_args()
			location = args['location']
			capacity = args['capacity']
			use = args['use']
			rooms = Room.insert(location,capacity,use)
		except:
			handle500error(rooms_ns)
		response = jsonify(rooms)
		return make_response(response,200)

@rooms_ns.route('/room/<ID>',methods=['GET','DELETE','OPTIONS'])

class ComputersInRoom(Resource):
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def get(self,ID):
		"""
		Returns all computer in a room
		"""
		try:
			rooms = Room.fetchComputersInRoom(ID)
		except:
			return handle500error(rooms_ns)
		response = jsonify(rooms)
		return make_response(response,200)

	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def delete(self,ID):
		"""
		Deletes a room
		"""
		try:
			rooms = Room.delete(ID)
		except:
			return handle500error(rooms_ns)
		response = jsonify(rooms)
		return make_response(response,200)
		
@rooms_ns.route('/room/unassigned/',methods=['GET','PUT','OPTIONS'])

class ComputersNotAssigned(Resource):

	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def get(self):
		"""
		Returns all computers not assigned to any room
		"""
		try:
			unassigned = Computer.fetchComputersUnassigned()
		except:
			return handle500error(rooms_ns)
		response = jsonify(unassigned)
		return make_response(response,200)

	@limiter.limit('1000/hour')
	@api.expect(room_computers_argument)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def put(self):
		"""
		Sets the computers assigned to the room
		"""
		try:
			args = room_computers_argument.parse_args()
			roomID = args['roomID']
			computers = args['computers']
			Room.setRoomIDFor(computers,roomID)
		except:
			return handle500error(rooms_ns)
		response = jsonify("Computers assigned")
		return make_response(response,200)