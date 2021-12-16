"""posts microservice for project 2"""
import hug
import os
from sqlite_utils import Database
import requests
import configparser
import socket
import greenstalk

# @hug.get('/posts/testFunction/{username}')
# def test(username, password):
#     db = Database("databases/Posts.db")
#     query = "SELECT username FROM users WHERE username = ? AND password = ?"
#     return db.query(query, (username, password))

config = configparser.ConfigParser()
config.read('api.ini')

svcrg_location = config['svcrg']['URL']  #'http://localhost:5400/svcrg/register'
url = 'localhost' # not working: socket.getfqdn()
port = os.environ['PORT']
requests.post(svcrg_location, data={'name': 'posts', 'URL': '{}:{}'.format(url,port)})

@hug.authentication.basic
def validate(username, password):
    #requestStr = 'http://localhost:5000/users/verify'
    
    svcrg_requestStr = svcrg_location[0:-8] # To remove the word 'register'
    svcrg_requestStr += 'users'
    
    response = requests.get(svcrg_requestStr)
    jsonObj = response.json()    
    users_requestStr = 'http://' + jsonObj['value'][0] + '/users/verify'
    

    r = requests.post(users_requestStr, data={'username': username, 'password': str(password)})
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
    query = "SELECT * FROM posts ORDER BY timestamp DESC"
    return {'result': db.query(query)}

# http GET '192.168.1.68:5000/posts/zachattack'


@hug.get('/posts/{username}')
def getUserTimeline(username):
    """Returns the timeline of posts for the user"""
    db = Database("databases/Posts.db")
    query = "SELECT * FROM posts WHERE username = ? ORDER BY timestamp DESC"
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

@hug.post('/posts/async', status=hug.falcon.HTTP.202, requires=validate)
def createPostAsync(response, hug.directives.user, text):
    """Inserts a new job to the message queue for creating a new post."""
    client = greenstalk.Client(('127.0.0.1', 11300))
    username = user['username']
    newPost = {'username': username, 'text': text}
    client.put(newPost)
    
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
		SELECT *
		FROM posts
		WHERE posts.username = {}
		ORDER BY timestamp DESC"""

    query = query.format(followerStr)
    return {'result': db.query(query)}

@hug.get('/posts/health-check')
def health_check(response):
	response.status = hug.falcon.HTTP_200
	return {'status': 'healthy'}
