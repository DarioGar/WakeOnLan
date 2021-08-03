from flask import jsonify, make_response
from flask_restx import cors
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_cors import cross_origin
from api.reusable import checkMAC,ping
from api.v1 import api
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.Computer import Computer
from api.models.Program import Program
from api.models.User import User
from api.mac_arguments import program_arguments,mac_arguments,allow_user_arguments,new_computer_arguments,update_computer_arguments
import schedule
import threading
import time

macs_ns = api.namespace('macs',description='Manages MACS for the users',decorators=[cors.crossdomain(origin="*")])

def computersOnline():
	while(True):
		online.clear()
		for computer in Computer.fetchAll():
			if (ping(computer[9])):
				online.append(computer[0])
		time.sleep(120)


programData = {}
online = []
job_thread = threading.Thread(target=computersOnline)
job_thread.start()

	
@macs_ns.route('/<mac>',methods=['POST','GET','DELETE','PUT','OPTIONS'])
class Computers(Resource):
	@cross_origin()
	@api.expect(new_computer_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self,mac):
		"""
		Adds a new computer
		"""
		try:
			args = new_computer_arguments.parse_args()
			computer = args['mac']
			ip = args['ip']
			ram = args['ram']
			cpu = args['cpu']
			gpu = args['gpu']
			os = args['os']
			ssd = args['ssd']
			owner = args['owner']
			responseData = Computer.insert(computer,ip,ram,cpu,gpu,os,ssd,owner)
			if(not responseData):
				response = jsonify("Succesfully inserted")
				return make_response(response,200)
			else:
				response = jsonify("Couldn't insert")
				return make_response(response,400)
		except:
			handle500error(macs_ns)

	@cross_origin()
	@api.expect(update_computer_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def put(self,mac):
		"""
		Updates a computer
		"""
		try:
			args = update_computer_arguments.parse_args()
			computer = args['mac']
			ip = args['ip']
			ram = args['ram']
			cpu = args['cpu']
			gpu = args['gpu']
			os = args['os']
			ssd = args['ssd']
			responseData = Computer.update(computer,ip,ram,cpu,gpu,os,ssd)
			if(not responseData):
				response = jsonify("Succesfully updated")
				return make_response(response,200)
			else:
				response = jsonify("Couldn't update")
				return make_response(response,404)
		except:
			handle500error(macs_ns)

	@cross_origin()
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def delete(self,mac):
		"""
		Deletes a computer
		"""
		try:

			responseData = Computer.delete(mac)
			if(not responseData):
				response = jsonify("Succesfully deleted")
				return make_response(response,200)
			else:
				response = jsonify("Couldn't delete")
				return make_response(response,404)
		except:
			handle500error(macs_ns)

@macs_ns.route('/for/<username>',methods=['GET','OPTIONS'])
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
			response = []
			computers = Computer.fetchComputerFor(username)
			for computer in computers:
				computer = list(computer)
				if(computer[7] in online):	
					computer.append(True)
				else:
					computer.append(False)
				response.append(computer)
			returnValue = jsonify(response)
			return make_response(returnValue,200)
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
			Computer.powerOn(MAC,username)
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
			users = User.fetchAll()
			allowedUsers = Computer.usersAllowedOn(mac)
			response = []
			for user in users:
				value = (user[0],False)
				for u in allowedUsers:
					if u[0] == user[5]:
						value = (user[0],True)
						break
				response.append(value)
			return make_response(jsonify(sorted(response, key=lambda tup: tup[1], reverse=True)),200)
		except:
			handle500error(macs_ns)

	@cross_origin()
	@api.expect(allow_user_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self,mac):
		"""
		Allows a user on a computer
		"""
		try:
			args = allow_user_arguments.parse_args()
			allowed = args['allowed']
			username = args['username']
			result = Computer.changeAllowed(username,allowed,mac)
			return make_response(result,200)
		except:
			handle500error(macs_ns)



@macs_ns.route('/log/<mac>',methods=['GET','POST','OPTIONS'])
class ComputerLog(Resource):
	@cross_origin()
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
			response = []
			computers = Computer.computersOf(username)
			for computer in computers:
				computer = list(computer)
				if(computer[7] in online):	
					computer.append(True)
				else:
					computer.append(False)
				response.append(computer)
			returnValue = jsonify(response)
			return make_response(returnValue,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/programs/<mac>',methods=['GET','POST','OPTIONS'])

class Programs(Resource):
	@cross_origin()
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def get(self,mac):
		"""
		Get the programs available for the computer
		"""
		try:
			programs = Program.getPrograms(mac)
			response = jsonify(programs)
			return make_response(response,200)
		except:
			handle500error(macs_ns)


	@cross_origin()
	@api.expect(program_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self,mac):
		"""
		Set the programs available for the computer
		"""
		try:
			args = program_arguments.parse_args()
			programs = args['programs']
			mac = args['computer']
			
			for program in programs:
				sliced = program.split('/')
				name = sliced[len(sliced)-1].split('.')[0]
				new = Program(name,program)
				Program.setPrograms(new,mac)
			returnValue = jsonify("response")
			return make_response(returnValue,200)
		except:
			handle500error(macs_ns)

@macs_ns.route('/programs/launch/<mac>',methods=['POST','OPTIONS'])

class ProgramsToLaunch(Resource):
	@cross_origin()
	@api.expect(program_arguments)
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	@jwt_required()
	def post(self):
		"""
		Sets the programs to be launched on power up
		"""
		try:
			args = program_arguments.parse_args()
			programs = args['programs']
			mac = args['computer']
			programData[mac]=[]
			for program in programs:
				programData[mac].append(program)
			returnValue = jsonify("Programs set launch" +programData[mac])
			return make_response(returnValue,200)
		except:
			handle500error(macs_ns)

	@cross_origin()
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def get(self,mac):
		"""
		Gets the programs to be launched on power up
		"""
		try:
			returnValue = jsonify(programData[mac])
			return make_response(returnValue,200)
		except:
			handle500error(macs_ns)
			