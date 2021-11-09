# foreman start --formation users=1,posts=3
users: gunicorn -b localhost:$PORT users:__hug_wsgi__
posts: gunicorn -b localhost:$PORT posts:__hug_wsgi__
