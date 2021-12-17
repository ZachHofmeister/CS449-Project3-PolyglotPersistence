"""worker program to insert new posts into the database"""
import greenstalk
from sqlite_utils import Database
import json

db = Database('databases/Posts.db')


def consume_message():
    while True:
        job = gsClient.reserve()
        jsonObj = json.loads(job.body)
        db["posts"].insert(jsonObj)
        print('hello from posts_worker')
        gsClient.put(job.body)
        gsClient.delete(job)
    
gsClient = greenstalk.Client(('127.0.0.1', 11300))
gsClient.watch('posts')
gsClient.use('polls')
consume_message()
