from flask_restx import reqparse

mac_arguments = reqparse.RequestParser()

mac_arguments.add_argument('username',
							location='json',
							type=str,
							required=True)

mac_arguments.add_argument('mac',
							location='json',
							type=str,
							required=True)