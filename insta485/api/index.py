"""REST API for v1."""
from multiprocessing import context
import flask
import insta485

@insta485.app.route('/api/v1/')
def service_list():
    context={
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url":"/api/v1/",
    }
    
    return flask.jsonify(**context)