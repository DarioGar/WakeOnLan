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

allow_user_arguments  = reqparse.RequestParser()

allow_user_arguments.add_argument('username',
							location='json',
							type=str,
							required=True)

allow_user_arguments.add_argument('allowed',
							location='json',
							type=bool,
							required=True)

new_computer_arguments = reqparse.RequestParser()

new_computer_arguments.add_argument('mac',
							location='json',
							type=str,
							required=True)

new_computer_arguments.add_argument('ip',
							location='json',
							type=str,
							required=True)
						
new_computer_arguments.add_argument('ram',
							location='json',
							type=str,
							required=True)

						
new_computer_arguments.add_argument('cpu',
							location='json',
							type=str,
							required=True)	

new_computer_arguments.add_argument('gpu',
							location='json',
							type=str,
							required=True)	

new_computer_arguments.add_argument('os',
							location='json',
							type=str,
							required=True)

new_computer_arguments.add_argument('ssd',
							location='json',
							type=str,
							required=True)

new_computer_arguments.add_argument('owner',
							location='json',
							type=str,
							required=True)

update_computer_arguments = reqparse.RequestParser()

update_computer_arguments.add_argument('mac',
							location='json',
							type=str,
							required=True)

update_computer_arguments.add_argument('ip',
							location='json',
							type=str,
							required=True)
						
update_computer_arguments.add_argument('ram',
							location='json',
							type=str,
							required=True)

						
update_computer_arguments.add_argument('cpu',
							location='json',
							type=str,
							required=True)	

update_computer_arguments.add_argument('gpu',
							location='json',
							type=str,
							required=True)	

update_computer_arguments.add_argument('os',
							location='json',
							type=str,
							required=True)

update_computer_arguments.add_argument('ssd',
							location='json',
							type=str,
							required=True)


program_arguments = reqparse.RequestParser()

program_arguments.add_argument('programs',
							location='json',
							type=list,
							required=True)

program_arguments.add_argument('computer',
							location='json',
							type=str,
							required=True)


