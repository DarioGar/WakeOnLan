from flask_restx import reqparse
# Argumentos que se esperan en la query en los distintos tipos HTTP
user_args_name_arguments = reqparse.RequestParser()

user_args_name_arguments.add_argument('username',
							location='args',
							type=str,
							required=True,
							help='User\'s username')

user_args_name_arguments.add_argument('password',
							location='args',
							type=str,
							required=True,
							help='User\'s encrypted password')

user_arguments = reqparse.RequestParser()

user_arguments.add_argument('username',
							location='args',
							type=str,
							required=True,
							help='User\'s username')

user_arguments.add_argument('information',
							location='json',
							type=dict,
							required=True,
							help='User information, crypted password, etc')

mac_arguments = reqparse.RequestParser()

mac_arguments.add_argument('username',
							location='headers',
							type=str,
							required=True)

mac_arguments.add_argument('MAC',
							location='headers',
							type=str,
							required=True)