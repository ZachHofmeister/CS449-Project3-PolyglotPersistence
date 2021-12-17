"""worker program to insert new posts into the database"""
import greenstalk
import configparser
import requests
import redis
import json

# db = Database('databases/Posts.db')


def consume_message():
    while True:
        job = client.reserve()
        postID = job.body
        postURL = postsIDUrl + postID
        response = requests.get(postURL)
        if not response:
            print(f'post id {postID} does not exist')
        client.delete(job)


config = configparser.ConfigParser()
config.read('api.ini')
svcrg_location = config['svcrg']['URL']
svcrg_requestStr = svcrg_location[0:-8] # To remove the word 'register'
svcrg_requestStr += 'posts'

response = requests.get(svcrg_requestStr)
jsonObj = response.json()    
postsIDUrl = 'http://' + jsonObj['value'][0] + '/posts/id/'

client = greenstalk.Client(('127.0.0.1', 11300))
# x = threading.Thread(target=consume_message, args=(), daemon=True)
# x.start()
consume_message()
