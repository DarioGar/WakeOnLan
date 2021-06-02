from flask_restx import reqparse

schedule_arguments = reqparse.RequestParser()

schedule_arguments.add_argument('computerId',
							location='json',
							type=str,
							required=True)

schedule_arguments.add_argument('username',
							location='json',
							type=str,
							required=True)

schedule_arguments.add_argument('days',
							location='json',
							type=list,
							required=True)

schedule_arguments.add_argument('time',
							location='json',
							type=str,
							required=True)