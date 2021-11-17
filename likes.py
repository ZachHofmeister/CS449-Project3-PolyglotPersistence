"""likes microservice for project 3"""
import hug
import redis

# http GET '192.168.1.68:5000/likes'

@hug.get('/likes/')
def getAllLikes():
	"""Returns all likes"""
	#Unimplimented
	r = redis.Redis(host='localhost', port=6379, db=0)
	r.set('foo', 'bar')
	return r.get('foo')

# http GET '192.168.1.68:5000/likes/popular'

@hug.get('/likes/popular/')
def getPopularPosts():
	"""Returns list of posts with more than 1 like"""
	#Unimplimented

# http GET '192.168.1.68:5000/likes/user/zachattack'

@hug.get('/likes/user/{username}')
def getUserLikes():
	"""Returns all the posts the user has liked"""
	#Unimplimented

# http GET '192.168.1.68:5000/likes/post/1'

@hug.get('/likes/post/{postID}')
def getPostLikes():
	"""Returns how many likes a post has received"""
	#Unimplimented

# http POST '192.168.1.68:5000/likes/post/1?username=willum'

@hug.post('/likes/post/{postID}', status=hug.falcon.HTTP_201)
def likePost(response, postID, username):
	"""Add a like from username to the post"""
	#Unimplimented