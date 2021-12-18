"""worker program to insert new posts into the database"""
import greenstalk
from sqlite_utils import Database
import json

db = Database('databases/Posts.db')

def consume_message():
    while True:
        job = gsClient.reserve()
        jsonObj = json.loads(job.body)
        #connection = sqlite3.connect('databases/Posts.db')
        #cursor = connection.cursor()
        #cursor.execute('INSERT INTO posts (username, text) VALUES (?,?)', (jsonObj['username'], jsonObj['text']))
        db["posts"].insert(jsonObj)
        #post_id = cursor.lastrowid
        #cursor.close()
        #connection.commit()
        #connection.close()
        #print('posts_worker inserted a new post with id: {}'.format(post_id))
        #newjsonObj = {'username': jsonObj['username'], 'text': jsonObj['text'], 'id': post_id}
        gsClient.put(job.body)
        gsClient.delete(job)
    
gsClient = greenstalk.Client(('127.0.0.1', 11300))
gsClient.watch('posts')
gsClient.use('polls')
consume_message()
