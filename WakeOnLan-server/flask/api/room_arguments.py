from flask_restx import reqparse

room_computers_argument = reqparse.RequestParser()

room_computers_argument.add_argument('roomID',
							location='json',
							type=str,
							required=True)

room_computers_argument.add_argument('computers',
							location='json',
							type=list,
							required=True)

new_room_argument = reqparse.RequestParser()

new_room_argument.add_argument('location',
							location='json',
							type=str,
							required=True)

new_room_argument.add_argument('capacity',
							location='json',
							type=int,
							required=True)

new_room_argument.add_argument('use',
							location='json',
							type=str,
							required=True)

