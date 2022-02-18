"""Utilities."""
import flask
import insta485
import insta485.views.auth


class InvalidUsage(Exception):
    """Exception API."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initialize Exception."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert to dictionary."""
        data = dict(self.payload or ())
        data['message'] = self.message
        data['status_code'] = self.status_code
        return data


@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle invalid usage."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def authentication():
    """Authenticate."""
    if flask.request.authorization is not None:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
        insta485.views.auth.login_account(username, password)
        return username
    if 'username' not in flask.session:
        raise InvalidUsage('Forbidden', 403)
    return flask.session['username']
