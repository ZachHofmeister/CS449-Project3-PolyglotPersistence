"""users microservice for project 2"""
import hug
from sqlite_utils import Database

# http GET 'localhost:5000/users'

@hug.get('/users/')
def getAllUsers():
	"""Returns all users"""
	db = Database("databases/Users.db")
	query = "SELECT * FROM users"
	return {'users': db.query(query)}

# http POST 'localhost:5000/users?username=testuser&email=test@user.com&password=321123'

@hug.post('/users/', status=hug.falcon.HTTP_201)
def createUser(response, username, email, password, bio=""):
	db = Database("databases/Users.db")
	newUser = {
		"username": username,
		"email": email,
		"password": password,
		"bio": bio
	}
	db["users"].insert(newUser)

	try:
		db["users"].insert(newUser)
	except Exception as e:
		response.status = hug.falcon.HTTP_409
		return {"error": str(e)}

	response.set_header("Location", f"/books/{username}")

	return newUser

# http GET 'localhost:5000/users/zachattack'
@hug.get('/users/{username}')
def getUser(username):
	"""Returns the profile info for the user"""
	db = Database("databases/Users.db")
	query = "SELECT username, email, bio FROM users WHERE username = ?"
	return {'user': db.query(query, (username,))}

# http GET 'localhost:5000/users/zachattack/following'
@hug.get('/users/{username}/following')
def getFollowing(username):
	"""Returns who the user is following"""
	db = Database("databases/Users.db")
	query = "SELECT friendname AS following FROM following WHERE followername = ?"
	return {'following': db.query(query, (username,))}

# http POST 'localhost:5000/users/joachim/following?following=zachattack'
@hug.post('/users/{username}/following', status=hug.falcon.HTTP_201)
def addFollowing(response, username, following):
	db = Database("databases/Users.db")
	user_id = getUserID(db, "users", username)
	following_id = getUserID(db, "users", following)

	newFollowing = {
		"follower_id": user_id,
		"following_id": following_id
	}

	try:
		db["followers"].insert(newFollowing)
	except Exception as e:
		response.status = hug.falcon.HTTP_409
		return {"error": str(e)}

	response.set_header("Location", f"/users/{username}/following")
	
	return newFollowing #TODO

# http DELETE 'localhost:5000/users/joachim/following?following=zachattack'
@hug.delete('/users/{username}/following')
def removeFollowing(response, username, following):
	db = Database("databases/Users.db")
	user_id = getUserID(db, "users", username)
	following_id = getUserID(db, "users", following)
	followers_row_id = getFollowersID(db, "followers", user_id, following_id)

	try:
		db["followers"].delete(followers_row_id)
	except Exception as e:
		response.status = hug.falcon.HTTP_409
		return {"error": str(e)}

	return {'result': f'User {username} is no longer following {following}'} #TODO

# http GET 'localhost:5000/users/zachattack/followers'
@hug.get('/users/{username}/followers')
def getFollowers(username):
	"""Returns who follows the user"""
	db = Database("databases/Users.db")
	query = "SELECT followername AS follower FROM following WHERE friendname = ?"
	return {'result': db.query(query, (username,))}

# http PUT 'localhost:5000/users/zachattack/changePassword?newPass=12346'
@hug.put('/users/{username}/changePassword')
def changePassword(username, newPass):
	db = Database("databases/Users.db")
	user_id = getUserID(db, "users", username)
	db["users"].update(user_id, {"password": newPass})
	return {'result': f'Successfully updated password for user: {username}'} #TODO

# http PUT 'localhost:5000/users/zachattack/changeBio?newBio=This is my new bio status'
@hug.put('/users/{username}/changeBio')
def changeBio(username, newBio):
	db = Database("databases/Users.db")
	user_id = getUserID(db, "users", username)

	db["users"].update(user_id, {"bio": newBio})
	return {'result': f'Successfully updated bio for user: {username}'} #TODO

# http POST 'localhost:5000/users/verify?username=zachattack&password=password'
@hug.post('/users/verify')
def verify_credentials(response, username: hug.types.text, password: hug.types.text):
        db = Database("databases/Posts.db")
        query = "SELECT username FROM users WHERE username = ? AND password = ?"
        user = []

        for row in db.query(query, (username, password)):
            user = row
        if not user:
            response.status = hug.falcon.HTTP_404
        return user

# helper functions

def getUserID(db, table, username):
	return next(db.query(f"SELECT id FROM {table} WHERE username = ?", (username,)))['id']

def getFollowersID(db, table, user_id, following_id):
	return next(db.query(f"SELECT id FROM {table} WHERE follower_id = ? AND following_id = ?", (user_id, following_id)))['id']
