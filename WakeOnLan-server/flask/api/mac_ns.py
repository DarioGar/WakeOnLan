from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_cors import cross_origin
from api.v1 import api
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.Computer import Computer

mac_ns = api.namespace('macs',description='Manages MACS for the users')


@mac_ns.route('/<username>',methods=['GET'])
class Assign(Resource):
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

@mac_ns.route('/<MAC>',methods=['GET','OPTIONS'])
class Assign(Resource):
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required
	def get(self,username):
		"""
		Returns all the information about the computer
		"""
		try:
			verify_jwt_in_request()
			claims = get_jwt()
			if claims["is_administrator"]:
				responseData = Computer.fetchAll()
		except:
			handle404error(mac_ns,'Unknown username')