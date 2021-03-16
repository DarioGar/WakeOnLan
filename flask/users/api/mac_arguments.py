from flask_restx import reqparse

mac_arguments = reqparse.RequestParser()

user_macs_arguments.add_argument('username',
							location='headers',
							type=str,
							required=True)

user_macs_arguments.add_argument('MAC',
							location='headers',
							type=str,
							required=True)