"""polls microservice for project 3"""
import hug
import boto3

dynamodb = None

# @hug.get('/polls/')
# def getAllPolls():
# 	"""Returns all polls"""
# 	#Unimplimented, not required

# http GET '192.168.1.68:5000/polls/zachattack/best breakfast'

@hug.get('/polls/{username}/{question}')
def getPollResults(response, username, question):
	global dynamodb
	if not dynamodb:
		dynamodb = boto3.resource(
			'dynamodb', endpoint_url='http://localhost:8000')
	table = dynamodb.Table('Polls')

	try:
		poll = table.get_item(
			Key={'username': username, 'question': question}
		)['Item']
	except Exception as e:
		print(f'exception in getPollResults: {str(e)}')
		response.status = hug.falcon.HTTP_404
	else:
		return poll


# http POST '192.168.1.68:5000/polls?username=zachattack&question=best breakfast&options=eggs,bacon,pancakes,waffles'

@hug.post('/polls/', status=hug.falcon.HTTP_201)
def createPoll(response, username, question, options):
	global dynamodb
	if not dynamodb:
		dynamodb = boto3.resource(
			'dynamodb', endpoint_url='http://localhost:8000')
	table = dynamodb.Table('Polls')

	voteCounts = [0 for _ in options]  # initialize array as zeros like options

	poll = {
		"username": username,
		"question": question,
		"info": {
			"options": options,
			"voteCounts": voteCounts,
			"usersVoted": []
		}
	}

	try:
		table.put_item(Item=poll)
	except Exception as e:
		print(f'exception in createPoll: {str(e)}')

	return poll


# http PUT '192.168.1.68:5000/polls/zachattack/best breakfast?voter=willum&vote=0'

@hug.put('/polls/{username}/{question}', status=hug.falcon.HTTP_200)
def votePoll(response, username, question, voter, vote):
	global dynamodb
	if not dynamodb:
		dynamodb = boto3.resource(
			'dynamodb', endpoint_url='http://localhost:8000')
	table = dynamodb.Table('Polls')

	try:
		poll = table.get_item(
			Key={'username': username, 'question': question}
		)['Item']
	except Exception as e:
		print(f'exception in getPollResults: {str(e)}')
		response.status = hug.falcon.HTTP_404
	else:
		if username in poll['info']['usersVoted']:
			response.status = hug.falcon.HTTP_409
			return 0
		else:
			response = table.update_item(
				Key={
					'username': username,
					'question': question
				},
				ConditionExpression=f'NOT contains(info.usersVoted, :voterName)',
				UpdateExpression=f'SET info.voteCounts[{vote}] = info.voteCounts[{vote}] + :val, info.usersVoted = list_append(info.usersVoted, :voter)',
				ExpressionAttributeValues={
					':val': 1,
					':voterName': voter,
					':voter': [voter]
				},
				ReturnValues="UPDATED_NEW"
			)
			return response
