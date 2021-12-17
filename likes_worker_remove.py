"""worker program to insert new posts into the database"""
import greenstalk
import configparser
import requests
import time
import json

# db = Database('databases/Posts.db')


def consume_message():
    svcrgResponse = None
    #Wait till svcrg is up and can give us the url for posts
    while not svcrgResponse:
        time.sleep(1)
        try:
            svcrgResponse = requests.get(svcrg_requestStr) #Exception if the request returns None, then svcrg isn't online yet.
            jsonObj = svcrgResponse.json()
        except:
            svcrgResponse = None 
        else:
            if not jsonObj['value']: #if svcrg is returning None, likes it isn't registered yet and we need to try again.
                svcrgResponse = None

    likesIDUrl = 'http://' + jsonObj['value'][0] + '/likes/post/'
    while True:
        job = gsClient.reserve()
        jobJson = json.loads(job.body)
        postID = jobJson['postID']
        username = jobJson['username']
        likeUrl = f'{likesIDUrl}{postID}?username={username}'
        print(likeUrl)
        requests.delete(likeUrl)
        gsClient.delete(job)


config = configparser.ConfigParser()
config.read('api.ini')
svcrg_location = config['svcrg']['URL']
svcrg_requestStr = svcrg_location[0:-8] # To remove the word 'register'
svcrg_requestStr += 'likes'

gsClient = greenstalk.Client(('127.0.0.1', 11300))
gsClient.watch('likesRemove')
print("starting consume message function")
consume_message()
