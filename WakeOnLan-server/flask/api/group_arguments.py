from flask_restx import reqparse

new_group_argument = reqparse.RequestParser()

new_group_argument.add_argument('groupLeader',
							location='json',
							type=str,
							required=True)

new_group_argument.add_argument('name',
							location='json',
							type=str,
							required=True)

new_group_argument.add_argument('path',
							location='json',
							type=str,
							required=True)

new_group_argument.add_argument('department',
							location='json',
							type=str,
							required=True)

room_argument = reqparse.RequestParser()

room_argument.add_argument('roomID',
							location='json',
							type=str,
							required=True)

room_argument.add_argument('groupID',
							location='json',
							type=str,
							required=True)