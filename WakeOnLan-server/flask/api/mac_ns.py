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

mac_ns = api.namespace('macs',description='Manages MACS for the users',decorators=[cors.crossdomain(origin="*")])


@mac_ns.route('/<username>',methods=['GET','OPTIONS'])
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
			handle500error(mac_ns)

@mac_ns.route('/mac',methods=['GET','POST','OPTIONS'])
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
			handle500error(mac_ns)