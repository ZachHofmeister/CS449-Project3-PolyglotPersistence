"""likes microservice for project 3"""
import hug
import redis

# http GET '192.168.1.68:5000/likes'

@hug.get('/likes/')
def getAllLikes():
	"""Returns all likes"""
	#Unimplimented, not asked for by prof but might be helpful
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
	"""
	When a user likes a post:
		Add the post id to a list stored in the key of their username
			ex key-value:	username: [0, 12, 20]
		Increment the number of likes stored in the key of the post ID
			ex key-value:	postID: #likes
		Update the number of likes for the post in the popular db
	"""
	userLikes = redis.Redis(host='localhost', port=6379, db=0)
	postLikes = redis.Redis(host='localhost', port=6379, db=1)
	popular = redis.Redis(host='localhost', port=6379, db=2)