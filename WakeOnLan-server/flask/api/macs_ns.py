from flask import jsonify, make_response
from flask_restx import cors
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_cors import cross_origin
from api.reusable import checkMAC
from api.v1 import api
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.Computer import Computer
from api.mac_arguments import mac_arguments
import schedule

macs_ns = api.namespace('macs',description='Manages MACS for the users',decorators=[cors.crossdomain(origin="*")])

@macs_ns.route('',methods=['POST','GET','OPTIONS'])
class Computers(Resource):
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
		Returns all the computers available for the user
		"""
		try:
			responseData = Computer.fetchComputerFor(username)
			response = jsonify(responseData)
			return make_response(response,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/<username>',methods=['GET','OPTIONS'])
class RetrieveComputers(Resource):
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
		Returns all the computers available for the user
		"""
		try:
			responseData = Computer.fetchComputerFor(username)
			response = jsonify(responseData)
			return make_response(response,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/power',methods=['GET','POST','OPTIONS'])
class PowerOn(Resource):
	@cross_origin()
	@api.expect(mac_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self):
		"""
		Sends a magic packet to the mac received
		"""
		try:
			args = mac_arguments.parse_args()
			MAC = args['mac']
			username = args['username']
			Computer.powerOn(MAC)
			response = jsonify("Trying to wake computer")
			return make_response(response,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/allowed/<mac>',methods=['GET','POST','OPTIONS'])
class UsersAllowed(Resource):
	@cross_origin()
	@api.expect(mac_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self,mac):
		"""
		Retrieves all the users and marks those that are allowed on this computer
		"""
		try:
			response = jsonify("")
			return make_response(response,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/log/<mac>',methods=['GET','POST','OPTIONS'])
class ComputerLog(Resource):
	@cross_origin()
	@api.expect(mac_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self,mac):
		"""
		Retrieves the bootup logs for the given computer 
		"""
		try:
			logs = Computer.logsFor(mac)
			response = jsonify(logs)
			return make_response(response,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/mac/<username>',methods=['GET','OPTIONS'])
class PersonalComputers(Resource):
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
		Get the personal computers for the given user
		"""
		try:
			computers = Computer.computersOf(username)
			response = jsonify(computers)
			return make_response(response,200)
		except:
			handle500error(macs_ns)