"""worker program to insert new posts into the database"""
import greenstalk
import configparser
import requests
import redis
import json

# db = Database('databases/Posts.db')


def consume_message():
    while True:
        print('hello world222')
        job = gsClient.reserve()

        # This should be a try/catch, or while loop to wait for svcrg connection
        svcrgResponse = requests.get(svcrg_requestStr)
        jsonObj = svcrgResponse.json()    
        postsIDUrl = 'http://' + jsonObj['value'][0] + '/posts/id/'

        postID = job.body
        postURL = postsIDUrl + postID
        print(postURL)
        postResponse = requests.get(postURL).json()
        print(postResponse)
        if not postResponse:
            print(f'post id {postID} does not exist')
        gsClient.delete(job)


config = configparser.ConfigParser()
config.read('api.ini')
svcrg_location = config['svcrg']['URL']
svcrg_requestStr = svcrg_location[0:-8] # To remove the word 'register'
svcrg_requestStr += 'posts'

gsClient = greenstalk.Client(('127.0.0.1', 11300))
gsClient.watch('likes')
print('hello world')
consume_message()
