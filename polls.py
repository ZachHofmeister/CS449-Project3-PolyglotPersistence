"""polls microservice for project 3"""
import hug

# @hug.get('/polls/')
# def getAllPolls():
# 	"""Returns all polls"""
# 	#Unimplimented, not required

# http GET '192.168.1.68:5000/polls/1'

@hug.get('/polls/{pollID}')
def getPollResults(response, pollID):
    #Unimplimented
	return 0

# http POST '192.168.1.68:5000/polls?username=zachattack&question=best breakfast&answers=["eggs", "bacon", "pancakes", "waffles"]'

@hug.post('/polls/', status=hug.falcon.HTTP_201)
def createPoll(response, username, question, resp):
	#Unimplimented
	return 0

# http PUT '192.168.1.68:5000/polls/1?username=zachattack&answer=0"

@hug.put('/polls/{pollID}', status=hug.falcon.HTTP_201)
def votePoll(response, pollID, username, answer):
	#Unimplimented
	return 0
