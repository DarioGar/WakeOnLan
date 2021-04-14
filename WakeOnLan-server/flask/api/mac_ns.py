from api.v1 import api
from flask_restx import Resource
from core import limiter, cache
from utils import handle400error, handle404error, handle500error

mac_ns = api.namespace('macs',description='Manages MACS for the users')

@mac_ns.route('/<username>/<MAC>')
class Assign(Resource):
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def post(self,username,MAC):
		"""
		Assigns a MAC for the user and adds the MAC if it is not already registered
		"""
		try:
			if username is not None:
				computers = list(db.computers.find({},{"_id" : 0 ,"MAC" : 1}))
				users = list(db.users.find({},{"_id" : 0 ,"username" : 1}))
				# We create a list of only the username field from the list of dictionaries returned from db.users.find()
				if username in [d['username'] for d in users]:
					if MAC not in [d['MAC'] for d in computers]:
						db.computers.insert_one({"MAC" : MAC})
					db.users.update_one({"username" : username},{ "$set" : {"assigned_macs" : MAC}})
					return "Asignada"
		except:
			handle404error(mac_ns,'Unknown username')
		handle500error(mac_ns)

	def get(self,username):
		"""
		Sends the magic package to all the MAC provided
		"""
		args = MAC_arguments.parse_args()

@mac_ns.route('/MAC')
class MAC(Resource):
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def get(self,username,MAC):
		"""
		Returns the information about the computer corresponding to the MAC: OS,processor, number of cores, frequency, RAM, and which GPU its using
		"""
		try:
			print("")
		except:
			handle404error(mac_ns,'Unknown username')

		handle500error(mac_ns)

	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def post(self,username,MAC):
		"""
		Adds a MAC and optionally all the information of the computer
		"""
		try:
			print("")
		except:
			handle404error(mac_ns,'Unknown username')
		handle500error(mac_ns)
