from flask_restx import reqparse

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