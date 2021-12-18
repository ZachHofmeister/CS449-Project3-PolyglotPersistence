"""worker program to validate polls in posts"""
import greenstalk
import configparser
import requests
import json
import time
import re
import smtplib

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
            if not jsonObj['value']: #if svcrg is returning None, posts it isn't registered yet and we need to try again.
                svcrgResponse = None


    pollsregex = 'http:\/\/[^/]+\/polls\/(\w+)\/(\w+)'
    print('pollsregex is {}'.format(pollsregex))
    while True:
        job = gsClient.reserve()
        jobObj = json.loads(job.body)
        matches = re.findall(pollsregex, jobObj['text'])
        print('matches is {}'.format(matches))
        
        for match in matches:
            link = 'http://{}/polls/{}/{}'.format(jsonObj['value'][0], match[0], match[1])
            print(link)
            try:
                r = requests.get(link)
            except Exception as e:
                print(e)
            else:
                if r.status_code is not requests.codes.ok:
                    print(job.body)
                    gsClient.put(job.body)
                    #notify the user by email
                    emailServer.sendmail("pollsVerifyWorker@localhost", "user@localhost", f'''
                        You attempted to link to a poll, with the id {pollID}, which does not exist.
                        Please do not attempt this any further.
                        Regards,
                        Polls Worker Verify
                    ''')                    
                    print('Not ok.')
                    break
                else:
                    print('ok.')
        gsClient.delete(job)
        
print('polls_worker_verify is running...')
config = configparser.ConfigParser()
config.read('api.ini')
svcrg_location = config['svcrg']['URL']
svcrg_requestStr = svcrg_location[0:-8] # To remove the word 'register'
svcrg_requestStr += 'polls'

gsClient = greenstalk.Client(('127.0.0.1', 11300))
gsClient.watch('polls')
gsClient.use('pollsRemove')
emailServer = smtplib.SMTP('localhost', port=1025)
emailServer.set_debuglevel(1)
consume_message()
