# foreman start --formation users=1,posts=3,likes=1,polls=1,svcrg=1,dynamoDB=1,posts_worker=1
users: gunicorn -b localhost:$PORT users:__hug_wsgi__
posts: gunicorn -b localhost:$PORT posts:__hug_wsgi__
likes: gunicorn -b localhost:$PORT likes:__hug_wsgi__
polls: gunicorn -b localhost:$PORT polls:__hug_wsgi__
svcrg: gunicorn -b localhost:$PORT svcrg:__hug_wsgi__
dynamoDB: java -Djava.library.path=./databases/dynamodb/DynamoDBLocal_lib -jar ./databases/dynamodb/DynamoDBLocal.jar -sharedDb
posts_worker: python3 posts_worker.py
