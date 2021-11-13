"""posts microservice for project 2"""
import hug
from sqlite_utils import Database
import requests

# @hug.get('/posts/testFunction/{username}')
# def test(username, password):
#     db = Database("databases/Posts.db")
#     query = "SELECT username FROM users WHERE username = ? AND password = ?"
#     return db.query(query, (username, password))

@hug.authentication.basic
def validate(username, password):
    requestStr = 'http://localhost:5000/users/verify'

    r = requests.post(requestStr, data={'username': username, 'password': str(password)})

    if r:
	    return username
    else:
	    return ''

# http GET 'localhost:5000/posts'

@hug.get('/posts/')
def getPublicTimeline():
    """Returns the timeline of posts from all users"""
    db = Database("databases/Posts.db")
    query = "SELECT username, text, timestamp, repost_url FROM posts ORDER BY timestamp DESC"
    return {'result': db.query(query)}

# http GET 'localhost:5000/posts/zachattack'

@hug.get('/posts/{username}')
def getUserTimeline(username):
    """Returns the timeline of posts for the user"""
    db = Database("databases/Posts.db")
    query = "SELECT username, text, timestamp, repost_url FROM posts WHERE username = ? ORDER BY timestamp DESC"
    return {'result': db.query(query, (username,))}

# http POST 'localhost:5000/posts?text=here is my new post'

@hug.post('/posts/', status=hug.falcon.HTTP_201, requires=validate)
def createPost(response, username: hug.directives.user, text):
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

# http GET 'localhost:5000/posts/zachattack/following'

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

# http GET 'localhost:5000/testAuth?username=zachattack&password=12345
# @authRequired.get('/testAuth')
# def testAuth(user: hug.directives.user):
# 	"""Authentication test"""
# 	db = Database("databases/Posts.db")

# 	return {'User': user} #TODO
