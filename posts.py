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
    # print(f"User: {username}, Pass: {password}")

    if r:
        return r.json()
    else:
        return []

# http GET '192.168.1.68:5000/posts'


@hug.get('/posts/')
def getPublicTimeline():
    """Returns the timeline of posts from all users"""
    db = Database("databases/Posts.db")
    query = "SELECT username, text, timestamp, repost_url FROM posts ORDER BY timestamp DESC"
    return {'result': db.query(query)}

# http GET '192.168.1.68:5000/posts/zachattack'


@hug.get('/posts/{username}')
def getUserTimeline(username):
    """Returns the timeline of posts for the user"""
    db = Database("databases/Posts.db")
    query = "SELECT username, text, timestamp, repost_url FROM posts WHERE username = ? ORDER BY timestamp DESC"
    return {'result': db.query(query, (username,))}

# http -a zachattack:password POST '192.168.1.68:5000/posts?text=here is my new post'

@hug.post('/posts/', status=hug.falcon.HTTP_201, requires=validate)
def createPost(response, user: hug.directives.user, text):
    """Posts the given text as the user"""
    db = Database("databases/Posts.db")

    username = user['username']
    newPost = {"username": username, "text": text}

    try:
        db["posts"].insert(newPost)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/posts/{username}")

    return newPost

# http -a zachattack:password GET '192.168.1.68:5000/posts/following'

@hug.get('/posts/following', requires=validate)
def getHomeTimeline(user: hug.directives.user):
    """Returns the timeline of posts from users that the user follows"""
    db = Database("databases/Posts.db")

    username = user['username']

    requestStr = "http://localhost:5000/users/{}/following".format(username)
    r = requests.get(requestStr)
    jsonObj = r.json()

    followerList = jsonObj['following']
    followerStr = ''

    for entry in followerList:
        followerStr += '\'{}\' OR posts.username = '.format(entry['following'])

    followerStr = followerStr[0:-3]  # To remove the last OR

    query = """
		SELECT posts.username, posts.text, posts.timestamp, posts.repost_url
		FROM posts
		WHERE posts.username = {}
		ORDER BY timestamp DESC"""

    query = query.format(followerStr)
    return {'result': db.query(query)}
