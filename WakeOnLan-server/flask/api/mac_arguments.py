from flask_restx import reqparse

mac_arguments = reqparse.RequestParser()

mac_arguments.add_argument('username',
							location='headers',
							type=str,
							required=True)

mac_arguments.add_argument('MAC',
							location='headers',
							type=str,
							required=True)