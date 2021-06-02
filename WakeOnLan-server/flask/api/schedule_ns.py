from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_cors import cross_origin
from api.v1 import api
from api.schedule_arguments import schedule_arguments
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.User import User
from api.models.Schedule import Schedule

schedule_ns = api.namespace('schedule',description='Manages the schedule for when the computers have to power up')


@schedule_ns.route('',methods=['GET','POST'])

class SchedulePowerUp(Resource):
	@limiter.limit('1000/hour')
	@api.expect(schedule_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	#@jwt_required()
	@cross_origin()
	def post(self):
		"""
		Registers time and days to power a computer
		"""
		try:
			args = schedule_arguments.parse_args()
			computer = args['computerId']
			days = args['days']
			time = args['time']
			user = args['username']
			userId = User.get(user)[0]
			schedule = Schedule(userId,computer,time,days)
			response = jsonify(schedule)
			return make_response(response,200)
		except:
			handle500error(schedule_ns)