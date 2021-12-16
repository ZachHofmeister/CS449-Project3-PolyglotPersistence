"""worker program to insert new posts into the database"""
import greenstalk
import threading
import time
from sqlite_utils import Database

def consume_message():
    job = client.reserve()
    jsonObj = job.body()
    db = Database('databases/Posts.db')
    db["posts"].insert(newPost)
    
client = greenstalk.Client(('127.0.0.1', 11300))    
x = threading.Thread(target=consume_message, args=(), daemon=True)
x.start()
