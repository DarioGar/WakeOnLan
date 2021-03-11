from api.v1 import api
from flask_restx import Resource
from core import limiter, cache

mac_ns = api.namespace('macs',description='Manages MACS for the users')

@mac_ns.route('/<username>/<MAC>')
class MAC(Resource):
	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def post(self,username,MAC):
		"""
		Adds a MAC for the user
		"""
		try:
			if username is not None and checkMAC(MAC):
				for user in usuarios:
					if username in user.values():
						user['MAC'] = [MAC]
						return user['MAC']
			else:		
				raise Exception('Invalid username or MAC address')
			raise Exception('Unknown username')
		except:
			handle404error(users_ns,'Unknown username')
		handle500error(users_ns)
