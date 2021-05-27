from flask_restx import reqparse

user_args_name_arguments = reqparse.RequestParser()

user_args_name_arguments.add_argument('username',
							location='json',
							type=str,
							required=True,
							help='User\'s username')

user_args_name_arguments.add_argument('password',
							location='json',
							type=str,
							required=True,
							help='User\'s password')

user_delete_arguments = reqparse.RequestParser()

user_delete_arguments.add_argument('username',
							location='args',
							type=str,
							required=True,
							help='User\'s username')

user_delete_arguments.add_argument('jwt',
							location='args',
							type=str,
							required=True,
							help='User\'s cookies')

new_user_arguments = reqparse.RequestParser()

new_user_arguments.add_argument('username',
							location='json',
							type=str,
							required=True,
							help='User\'s username')

new_user_arguments.add_argument('fullname',
							location='json',
							type=str,
							required=True,
							help='User full name')

new_user_arguments.add_argument('password',
							location='json',
							type=str,
							required=True,
							help='User password')

new_user_arguments.add_argument('role',
							location='json',
							type=str,
							required=True,
							help='User role')

new_user_arguments.add_argument('email',
							location='json',
							type=str,
							required=True,
							help='User email')