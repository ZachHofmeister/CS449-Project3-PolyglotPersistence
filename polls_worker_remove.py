"""worker program to remove posts containing invalid polls from the database"""
import greenstalk
import configparser
import json
from sqlite_utils import Database

db = Database('databases/Posts.db')

def consume_message():
    #query = 'DELETE FROM posts WHERE id == {}'
    #select_query = 'SELECT * FROM posts WHERE username == \'{}\'' #AND text == \'{}\''
    while True:
        job = gsClient.reserve()
        jobObj = json.loads(job.body)
        #query = query.format(jobObj['username'], jobObj['text'])
        #query = query.format(jobObj['id'])
        #select_query = select_query.format(jobObj['username'])
        #print('select query is: {}'.format(select_query))
        #print('delete query is: {}'.format(query))
        
        #for row in db.query(select_query):
            #print(row)
        #db.execute(query)
        gsClient.delete(job)
        

print('polls_worker_remove is running...')
config = configparser.ConfigParser()
config.read('api.ini')
svcrg_location = config['svcrg']['URL']
svcrg_requestStr = svcrg_location[0:-8] # To remove the word 'register'
svcrg_requestStr += 'polls'

gsClient = greenstalk.Client(('127.0.0.1', 11300))
gsClient.watch('pollsRemove')
consume_message()
