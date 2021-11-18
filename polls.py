"""polls microservice for project 3"""
import hug
import boto3

# @hug.get('/polls/')
# def getAllPolls():
# 	"""Returns all polls"""
# 	#Unimplimented, not required

# http GET '192.168.1.68:5000/polls/1'

@hug.get('/polls/{pollID}')
def getPollResults(response, pollID):
    #Unimplimented
	return 0

# http POST '192.168.1.68:5000/polls?username=zachattack&question=best breakfast&answers=['eggs', 'bacon', 'pancakes', 'waffles']'

@hug.post('/polls/', status=hug.falcon.HTTP_201)
def createPoll(response, username, question, resp):
	#Unimplimented
	return 0

# http PUT '192.168.1.68:5000/polls/1?username=zachattack&answer=0'

@hug.put('/polls/{pollID}', status=hug.falcon.HTTP_200)
def votePoll(response, pollID, username, answer):
	#Unimplimented
	return 0

#Helper functions

#this should run on startup to fetch the table item
def create_polls_table(dynamodb = None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

	try:
		table = dynamodb.create_table(
			TableName='Polls',
			KeySchema=[
				{
					'AttributeName': 'id',
					'KeyType': 'HASH' #partition key
				},
				{
					'AttributeName': 'username',
                	'KeyType': 'RANGE'  #sort key
				}
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'id',
					'AttributeType': 'N' #number
				},
				{
					'AttributeName': 'username',
					'AttributeType': 'S' #string
				},
				{
					'AttributeName': 'question',
					'AttributeType': 'S' #string
				},
				{
					'AttributeName': 'answers',
					'AttributeType': 'SS' #string set
				},
				{
					'AttributeName': 'voteCounts',
					'AttributeType': 'NS' #number set
				},
				{
					'AttributeName': 'usersVoted',
					'AttributeType': 'SS' #string set
				},
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 10,
				'WriteCapacityUnits': 10
			}
		)
	except Exception as e:
		# print(f'exception in create_polls_table: {str(e)}')
		table = dynamodb.Table('Polls')
	
	return table