"""worker program to insert new posts into the database"""
import greenstalk
import threading
import time
from sqlite_utils import Database

db = Database('databases/Posts.db')

def consume_message():
    while True:
        job = client.reserve()
        jsonObj = job.body()
        db["posts"].insert(newPost)
        client.delete(job)
    
client = greenstalk.Client(('127.0.0.1', 11300))    
x = threading.Thread(target=consume_message, args=(), daemon=True)
x.start()
