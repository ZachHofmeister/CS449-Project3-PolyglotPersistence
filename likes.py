"""likes microservice for project 3"""
import hug
import redis
import os
import requests
import configparser

# https://redis-py.readthedocs.io/en/stable/

# http GET '192.168.1.68:5000/likes'

# @hug.get('/likes/')
# def getAllLikes():
# 	"""Returns all likes"""
# 	#Unimplimented, not asked for by prof but might be helpful
# 	r = redis.Redis(host='localhost', port=6379, db=0)
# 	r.set('foo', 'bar')
# 	return r.get('foo')

userDB = 0
postDB = 1
popularDB = 2

config = configparser.ConfigParser()
config.read('api.ini')

requestStr = config['svcrg']['URL']  #'http://localhost:5400/svcrg/register'
port = os.environ['PORT']
requests.post(requestStr, data={'name': 'likes', 'URL': 'localhost:{}'.format(port)})

# http GET '192.168.1.68:5000/likes/popular'

@hug.get('/likes/popular/')
def getPopularPosts(response):
	"""Returns list of top 10 posts"""
	popular = redis.Redis(host='localhost', port=6379, db=popularDB)
	postList = popular.zrevrange("popular", 0, 9, withscores=True)

	#change key labels to be descriptive
	for index, post in enumerate(postList):
		postList[index] = {"post-id": post[0], "likes": post[1]}

	return {"popular": postList}

# http GET '192.168.1.68:5000/likes/user/zachattack'

@hug.get('/likes/user/{username}')
def getUserLikes(response, username):
	"""Returns all the posts the user has liked"""
	userLikes = redis.Redis(host='localhost', port=6379, db=userDB)
	return {"posts": userLikes.smembers(username)}

# http GET '192.168.1.68:5000/likes/post/1'

@hug.get('/likes/post/{postID}')
def getPostLikes(postID):
	"""Returns how many likes a post has received"""
	postLikes = redis.Redis(host='localhost', port=6379, db=postDB)
	return {"likes": postLikes.get(postID)}

# http POST '192.168.1.68:5000/likes/post/1?username=willum'

@hug.post('/likes/post/{postID}', status=hug.falcon.HTTP_201)
def likePost(response, postID, username):
	"""Add a like from username to the post"""
	"""
	When a user likes a post:
		Add the post id to a list stored in the key of their username
			ex key-value:	username: [0, 12, 20]
		Increment the number of likes stored in the key of the post ID
			ex key-value:	postID: #likes
		Update the number of likes for the post in the popular db
	"""
	#maybe TODO: Should verify that username and postID exists

	userLikes = redis.Redis(host='localhost', port=6379, db=userDB)
	if userLikes.sismember(username, postID):
		response.status = hug.falcon.HTTP_409
		return {"error": f"{username} has already liked post {postID}"}
	
	userLikes.sadd(username, postID)

	postLikes = redis.Redis(host='localhost', port=6379, db=postDB)
	postLikes.incrby(postID)

	popular = redis.Redis(host='localhost', port=6379, db=popularDB)
	popular.zincrby("popular", 1, postID)

	response.set_header("Location", f"/likes/post/{postID}")
	return getPostLikes(postID=postID)

@hug.get('/likes/health-check')
def health_check(response):
	response.status = hug.falcon.HTTP_200
	return {'status': 'healthy'}
