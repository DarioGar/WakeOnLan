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


update_user_arguments = reqparse.RequestParser()

update_user_arguments.add_argument('username',
							location='json',
							type=str,
							required=True,
							help='User\'s username')

update_user_arguments.add_argument('fullname',
							location='json',
							type=str,
							required=True,
							help='User full name')

update_user_arguments.add_argument('password',
							location='json',
							type=str,
							required=True,
							help='User password')

update_user_arguments.add_argument('role',
							location='json',
							type=str,
							required=True,
							help='User role')

update_user_arguments.add_argument('email',
							location='json',
							type=str,
							required=True,
							help='User email')

update_user_arguments.add_argument('pw',
							location='json',
							type=bool,
							required=True,
							help='Is the password being changed? True or False')							

invite_user_arguments = reqparse.RequestParser()

invite_user_arguments.add_argument('sender',
							location='json',
							type=str,
							required=True,
							help='Name of the user inviting')

invite_user_arguments.add_argument('to',
							location='json',
							type=str,
							required=True,
							help='Name of the user to invite')

invite_user_arguments.add_argument('group',
							location='json',
							type=str,
							required=True,
							help='Group ID the user got invited to')

manage_invite_user_arguments = reqparse.RequestParser()

manage_invite_user_arguments.add_argument('id',
							location='json',
							type=str,
							required=True,
							help='ID of the invitation')

manage_invite_user_arguments.add_argument('groupId',
							location='json',
							type=str,
							required=False,
							help='ID of the work_group the user is managing')

manage_invite_user_arguments.add_argument('userId',
							location='json',
							type=str,
							required=False,
							help='ID of the user')