"""
Insta485 authentication.

URLs include:
/accounts/login/
/accounts/logout/
/accounts/create/
/accounts/delete/
/accounts/edit/
/accounts/password/
/accounts/?target=URL
"""
import os

import flask
import insta485
from insta485.views.utility import hash_password, user_exists_in_database, \
    save_file, get_profile_pic
import insta485.api.utility


@insta485.app.route('/accounts/login/')
def login():
    """Display / route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Display / route."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/accounts/create/')
def create():
    """Display / route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit'))
    return flask.render_template("create.html")


@insta485.app.route('/accounts/delete/')
def delete():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    context = {'logname': logname}
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/edit/')
def edit():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT fullname, email, filename FROM users "
        "WHERE username == ?",
        (logname, )
    )

    dic = cur.fetchall()[0]
    fullname = dic['fullname']
    email = dic['email']
    filename = dic['filename']

    context = {'logname': logname, 'fullname': fullname, 'email': email,
               'filename': filename,
               'current_url': flask.request.path}
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/')
def edit_password():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    context = {'logname': logname}
    return flask.render_template("password.html", **context)


@insta485.app.route('/accounts/', methods=['POST'])
def edit_account():
    """Display / route."""
    operation = flask.request.values.get('operation')

    if operation == 'login':
        username = flask.request.values.get('username')
        password = flask.request.values.get('password')
        login_account(username, password)
        flask.session['username'] = username
    elif operation == 'create':
        create_account()
    elif operation == 'delete':
        delete_account()
    elif operation == 'edit_account':
        change_account()
    elif operation == 'update_password':
        update_password()

    if flask.request.args.get('target'):
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_index'))


def login_account(username, password):
    """Login account."""
    if not username or not password:
        raise insta485.api.utility.InvalidUsage("Bad Request", 400)

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password FROM users "
        "WHERE username == ?",
        (username,)
    )
    result = cur.fetchall()
    if len(result) == 0:
        raise insta485.api.utility.InvalidUsage("Forbidden", 403)

    hashed_password = result[0]['password']
    salt = hashed_password.split('$')[1]
    password = hash_password(password, salt)
    if result[0]['password'] != password:
        raise insta485.api.utility.InvalidUsage("Forbidden", 403)


def create_account():
    """Create account."""
    username = flask.request.values.get('username')
    password = flask.request.values.get('password')
    fullname = flask.request.values.get('fullname')
    email = flask.request.values.get('email')
    file = flask.request.files.get('file')
    if not (username and password and fullname and email and file):
        flask.abort(400)
    if user_exists_in_database(username):
        flask.abort(409)

    password = hash_password(password)
    filename = save_file(file)
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO users(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, filename, password,)
    )

    flask.session['username'] = username


def delete_account():
    """Delete account."""
    if 'username' not in flask.session:
        flask.abort(403)
    logname = flask.session['username']

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename FROM posts "
        "WHERE owner == ?",
        (logname,)
    )
    content = cur.fetchall()
    filenames = [d['filename'] for d in content]
    for filename in filenames:
        path = insta485.app.config["UPLOAD_FOLDER"] / filename
        os.remove(path)

    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username == ?",
        (logname,)
    )
    filename = cur.fetchone()['filename']
    path = insta485.app.config["UPLOAD_FOLDER"] / filename
    os.remove(path)

    connection.execute(
        "DELETE FROM users "
        "WHERE username == ?",
        (logname,)
    )

    flask.session.clear()


def change_account():
    """Change account."""
    if 'username' not in flask.session:
        flask.abort(403)
    logname = flask.session['username']

    fullname = flask.request.values.get('fullname')
    email = flask.request.values.get('email')
    file = flask.request.files.get('file')
    if not fullname or not email:
        flask.abort(400)

    if file:
        filename = save_file(file)
        connection = insta485.model.get_db()
        old_filename = get_profile_pic(logname)
        path = insta485.app.config["UPLOAD_FOLDER"] / old_filename
        os.remove(path)
        connection.execute(
            "UPDATE users "
            "SET (fullname, email, filename) = (?, ?, ?)"
            "WHERE username == ?",
            (fullname, email, filename, logname,)
        )
    else:
        connection = insta485.model.get_db()
        connection.execute(
            "UPDATE users "
            "SET (fullname, email) = (?, ?)"
            "WHERE username == ?",
            (fullname, email, logname,)
        )


def update_password():
    """Update password."""
    if 'username' not in flask.session:
        flask.abort(403)
    logname = flask.session['username']

    password = flask.request.values.get('password')
    new_password1 = flask.request.values.get('new_password1')
    new_password2 = flask.request.values.get('new_password2')
    if not password or not new_password1 or not new_password2:
        flask.abort(400)

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password FROM users "
        "WHERE username == ?",
        (logname,)
    )
    old_password = cur.fetchone()['password']
    password = hash_password(password, old_password.split('$')[1])
    if password != old_password:
        flask.abort(403)
    if new_password1 != new_password2:
        flask.abort(401)

    new_password = hash_password(new_password1)
    connection.execute(
        "UPDATE users "
        "SET password = ?"
        "WHERE username == ?",
        (new_password, logname,)
    )
