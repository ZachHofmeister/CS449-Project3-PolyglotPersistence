# foreman start --formation users=1,posts=3,likes=1,polls=1,svcrg=1,dynamoDB=1,posts_worker=1,likes_verify=1,likes_remove=1,polls_verify=1,polls_remove=1,emailServer=1
users: gunicorn -b localhost:$PORT users:__hug_wsgi__
posts: gunicorn -b localhost:$PORT posts:__hug_wsgi__
likes: gunicorn -b localhost:$PORT likes:__hug_wsgi__
polls: gunicorn -b localhost:$PORT polls:__hug_wsgi__
svcrg: gunicorn -b localhost:$PORT svcrg:__hug_wsgi__
dynamoDB: java -Djava.library.path=./databases/dynamodb/DynamoDBLocal_lib -jar ./databases/dynamodb/DynamoDBLocal.jar -sharedDb
posts_worker: python3 posts_worker.py
likes_verify: python3 likes_worker_verify.py
likes_remove: python3 likes_worker_remove.py
polls_verify: python3 polls_worker_verify.py
polls_remove: python3 polls_worker_remove.py
emailServer: python -m smtpd -n -c DebuggingServer localhost:1025
