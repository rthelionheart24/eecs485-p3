"""
Insta485 utility.

URLs include:
/uploads/<filename>
"""
import hashlib
import pathlib
import uuid

import flask
import insta485


@insta485.app.route('/uploads/<filename>')
def download_file(filename):
    """Download file."""
    if 'username' not in flask.session:
        flask.abort(403)
    return flask.send_from_directory(
        insta485.app.config['UPLOAD_FOLDER'], filename, as_attachment=True
    )


def get_following_list(username):
    """Get following list."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 == ?",
        (username,)
    )
    following_list = [d['username2'] for d in cur.fetchall()]
    return following_list


def get_followers_list(username):
    """Get followers list."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username2 == ?",
        (username,)
    )
    followers_list = [d['username1'] for d in cur.fetchall()]
    return followers_list


def get_profile_pic(username):
    """Get profile picture for username."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username == ?",
        (username, )
    )
    return cur.fetchall()[0]['filename']


def user_exists_in_database(username):
    """Check whether user exists in the database."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users "
        "WHERE username == ?",
        (username,)
    )
    return len(cur.fetchall()) != 0


def follows(username1, username2):
    """Check whether user1 follows user2."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE (username1, username2) == (?, ?)",
        (username1, username2)
    )
    return len(cur.fetchall()) != 0


def hash_password(password, salt=uuid.uuid4().hex):
    """Hash the password with a salt."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def save_file(file):
    """Save the file in system."""
    filename = file.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(path)
    return uuid_basename
