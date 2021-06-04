from flask import jsonify, make_response
from flask_restx import cors
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
from api.models.Computer import Computer
from api.models.Schedule import Schedule
import schedule
import time

schedule_ns = api.namespace('schedule',description='Manages the schedule for when the computers have to power up',decorators=[cors.crossdomain(origin="*")])


@schedule_ns.route('',methods=['GET','POST','OPTIONS'])

class SchedulePowerUp(Resource):
	@limiter.limit('1000/hour')
	@api.expect(schedule_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	@cross_origin()
	def post(self):
		"""
		Registers time and days to power a computer
		"""
		result = 0
		try:
			args = schedule_arguments.parse_args()
			computer = args['computerId']
			days = args['days']
			time = args['time']
			user = args['username']
			userId = User.get(user)[0]
			scheduleobj = Schedule(userId,computer,time,days)
		except:
			handle400error(schedule_ns,"The provided arguments are not correct. Please, check the swagger documentation at /v1")
		try:
			result = scheduleobj.insert()[0]
			computer = Computer.fetch(computer)
			#computer[2] has the mac
			for day in days:
				print(day)
				print(schedule.get_jobs())
				if day.lower() == "monday":
					schedule.every().monday.at(time).do(Computer.powerOn,computer[2])
				elif day.lower() == "tuesday":
					schedule.every().tuesday.at(time).do(Computer.powerOn,computer[2])
				elif day.lower() == "wednesday":
					schedule.every().wednesday.at(time).do(Computer.powerOn,computer[2])
				elif day.lower() == "thursday":
					schedule.every().thursday.at(time).do(Computer.powerOn,computer[2])
				elif day.lower() == "friday":
					schedule.every().friday.at(time).do(Computer.powerOn,computer[2])
				elif day.lower() == "saturday":
					schedule.every().saturday.at(time).do(Computer.powerOn,computer[2])
				elif day.lower() == "sunday":
					schedule.every().sunday.at(time).do(Computer.powerOn,computer[2])
		except:
			handle500error(schedule_ns)
		response = jsonify(result)
		return make_response(response,200)
		