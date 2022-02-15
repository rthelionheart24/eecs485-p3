"""Utilities."""
import flask
import insta485
from insta485.views.auth import login_account


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def authentication():
    # Authentication
    if flask.request.authorization is not None:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
        login_account(username, password)
        return username
    elif 'username' not in flask.session:
        raise InvalidUsage('Forbidden', 403)
    else:
        return flask.session['username']
