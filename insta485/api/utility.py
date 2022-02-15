"""Utilities."""
import flask
from insta485.views.auth import login_account


def authentication():
    # Authentication
    username = flask.request.authorization['username']
    password = flask.request.authorization['password']
    if username and password:
        login_account(username, password)
        return username
    elif 'username' not in flask.session:
        flask.abort(403)
    else:
        return flask.session['username']
