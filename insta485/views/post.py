"""
Insta485 post view.

URLs include:
/posts/<postid_url_slug>
/posts/?target=URL
/likes/?target=URL
/comments/?target=URL
"""
import os

import arrow
import flask
import insta485
from insta485.views.utility import get_profile_pic, save_file


@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    """Display / route."""
    if 'username' in flask.session:
        logname = flask.session['username']
    else:
        return flask.redirect(flask.url_for('login'))

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM posts "
        "WHERE postid == ?",
        (postid_url_slug, )
    )
    pst = cur.fetchall()[0]

    cur = connection.execute(
        "SELECT * FROM comments "
        "WHERE postid == ?",
        (pst['postid'],)
    )
    pst['comments'] = cur.fetchall()
    pst['owner_img_url'] = get_profile_pic(pst['owner'])
    cur = connection.execute(
        "SELECT owner FROM likes "
        "WHERE postid == ?",
        (pst['postid'],)
    )
    liked_users = cur.fetchall()
    pst['likes'] = len(liked_users)
    pst['liked'] = logname in [d['owner'] for d in liked_users]
    pst['created'] = arrow.get(pst['created']).humanize()
    current_url = flask.request.path if flask.request.path \
        else flask.url_for('show_index')
    context = {"logname": logname, "post": pst,
               "current_url": current_url,
               "logged_in_user_url": flask.url_for('show_user',
                                                   user_url_slug=logname)}
    return flask.render_template("post.html", **context)


@insta485.app.route('/posts/', methods=['POST'])
def edit_post():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']
    operation = flask.request.values.get('operation')
    connection = insta485.model.get_db()

    if operation == 'create':
        file = flask.request.files.get('file')
        if not file:
            flask.abort(400)
        filename = save_file(file)
        connection.execute(
            "INSERT INTO posts(filename, owner)"
            "VALUES (?, ?)",
            (filename, logname, )
        )

    elif operation == 'delete':
        postid = flask.request.values.get('postid')
        cur = connection.execute(
            "SELECT owner, filename from posts "
            "WHERE postid == ?",
            (postid, )
        )
        content = cur.fetchone()
        if content['owner'] != logname:
            flask.abort(403)
        old_filename = content['filename']
        path = insta485.app.config["UPLOAD_FOLDER"] / old_filename
        os.remove(path)
        connection.execute(
            "DELETE FROM posts "
            "WHERE postid == ?",
            (postid, )
        )

    if flask.request.args.get('target'):
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_user', user_url_slug=logname))


@insta485.app.route('/likes/', methods=['POST'])
def edit_likes():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']
    operation = flask.request.values.get('operation')
    postid = flask.request.values.get('postid')
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM likes "
        "WHERE owner == ? AND postid == ?",
        (logname, postid, )
    )
    content = cur.fetchall()
    if len(content) == 0 and operation == 'unlike':
        flask.abort(409)
    if len(content) == 1 and operation == 'like':
        flask.abort(409)

    if operation == 'like':
        connection.execute(
            "INSERT INTO likes(owner, postid)"
            "VALUES (?, ?)",
            (logname, postid, )
        )
    elif operation == 'unlike':
        connection.execute(
            "DELETE FROM likes "
            "WHERE owner == ? AND postid == ?",
            (logname, postid, )
        )
    if flask.request.args.get('target'):
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_index'))


@insta485.app.route('/comments/', methods=['POST'])
def edit_comment():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']
    operation = flask.request.values.get('operation')
    connection = insta485.model.get_db()
    if operation == 'create':
        postid = flask.request.values.get('postid')
        text = flask.request.values.get('text')
        if not text:
            flask.abort(400)
        connection.execute(
            "INSERT INTO comments(owner, postid, text)"
            "VALUES (?, ?, ?)",
            (logname, postid, text, )
        )
    elif operation == 'delete':
        commentid = flask.request.values.get('commentid')
        cur = connection.execute(
            "SELECT owner from comments "
            "WHERE commentid == ?",
            (commentid, )
        )
        if cur.fetchone()['owner'] != logname:
            flask.abort(403)
        connection.execute(
            "DELETE FROM comments "
            "WHERE commentid == ?",
            (commentid, )
        )
    if flask.request.args.get('target'):
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_index'))
