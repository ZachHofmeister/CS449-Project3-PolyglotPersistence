"""posts microservice for project 2"""
import hug
from sqlite_utils import Database

#http GET 'localhost:5000/posts'
@hug.get('/posts/')
def getPublicTimeline():
	"""Returns the timeline of posts from all users"""
	db = Database("databases/Posts.db")
	query = "SELECT username, text, timestamp, repost_url FROM posts ORDER BY timestamp DESC"
	return {'result': db.query(query)}

#http GET 'localhost:5000/posts/zachattack'
@hug.get('/posts/{username}')
def getUserTimeline(username):
	"""Returns the timeline of posts for the user"""
	db = Database("databases/Posts.db")
	query = "SELECT username, text, timestamp, repost_url FROM posts WHERE username = ? ORDER BY timestamp DESC"
	return {'result': db.query(query, (username,))}

#http POST 'localhost:5000/posts/zachattack?text=here is my new post'
@hug.post('/posts/{username}', status=hug.falcon.HTTP_201)
def createPost(response, username, text):
	"""Posts the given text as the user"""
	db = Database("databases/Posts.db")

	newPost = {"username": username, "text": text}

	try:
		db["posts"].insert(newPost)
	except Exception as e:
		response.status = hug.falcon.HTTP_409
		return {"error": str(e)}

	response.set_header("Location", f"/posts/{username}")

	return newPost

#http GET 'localhost:5000/posts/zachattack/following'
@hug.get('/posts/{username}/following')
def getHomeTimeline(username):
	"""Returns the timeline of posts from users that the user follows"""
	db = Database("databases/Posts.db")
	query = """
		SELECT posts.username, posts.text, posts.timestamp, posts.repost_url
		FROM posts, following
		WHERE following.followername = ?
			AND posts.username = following.friendname
		ORDER BY timestamp DESC"""
	return {'result': db.query(query, (username,))}

# authRequired = hug.http(requires=hug.authentication.basic(
# 	hug.authentication.verify("zach", "1234")
# ))

#http GET 'localhost:5000/testAuth?username=zachattack&password=12345
# @authRequired.get('/testAuth')
# def testAuth(user: hug.directives.user):
# 	"""Authentication test"""
# 	db = Database("databases/Posts.db")

# 	return {'User': user} #TODO

"""
**`getUserTimeline(username)`**

> ```shell-session
> $ http GET 'localhost:5100/posts/?username=ProfAvery&sort=-timestamp'
> ```

**`getPublicTimeline()`**

> ```shell-session
> $ http GET localhost:5100/posts/?sort=-timestamp
> ```

**`getHomeTimeline(username)`**

> ```shell-session
> $ friends=$(http GET 'localhost:5200/users/following.json?_facet=username&username=ProfAvery&_shape=array' | jq --raw-output 'map(.friendname) | join(",")')
> $ http GET "http://localhost:5300/timelines/posts.json?_sort_desc=timestamp&_shape=array&username__in=$friends"
> ```

**`postTweet(username, text)`**

> ```shell-session
> $ http POST localhost:5100/posts/ username=tester text='This is a test.'
> ```
"""