"""service registry microservice for project 3"""
import hug
import threading
import time
import requests

# DB = {'users': ['localhost:5000'],
#       'posts': [localhost:5100', 'localhost:5101' 'localhost:5102'],
#       ...
#      }
DB = {}

def health_checkup():
	time.sleep(10)
	print("health check")
	lock = threading.Lock()
	values_to_del = {}
	for key, value in DB.items():
		for instance in value:
			requestStr = 'http://{}/{}/health-check'.format(instance, key)

			try:
				r = requests.get(requestStr)
			except Exception as e:
				values_to_del[key] = instance
			else:
				if r.status_code is not requests.codes.ok:
					values_to_del[key] = instance

	with lock:
		for key, value in values_to_del.items():
			print('{} at {} is unhealthy. Deleting.'.format(key, value))
			newList = DB[key].remove(value)
			if not newList:
				del DB[key]
			else:
				DB[key] = newList

x = threading.Thread(target=health_checkup, args=(), daemon=True)
x.start()

# http GET '192.168.1.68:5000/svcrg'

@hug.get('/svcrg/')
def getAllServices():
	"""Returns all services"""
	return DB

# http POST '192.168.1.68:5000/svcrg/register?name=users&URL=localhost:5000'
@hug.post('/svcrg/register')
def register(response, name, URL):
	lock = threading.Lock()
	with lock:
		if DB.get(name):
			DB[name].append(URL)
		else:
			DB[name] = [URL]
		
		return {name: DB[name]}

# http GET '192.168.1.68:5000/svcrg/users'
@hug.get('/svcrg/{name}')
def getServiceByName(response, name):
	return {'value': DB.get(name)}
