"""
Insta485 user view.

URLs include:
/users/<user_url_slug>/
"""
import flask
import insta485
from insta485.views.utility import user_exists_in_database, follows, \
    get_profile_pic, get_following_list, get_followers_list


@insta485.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    if not user_exists_in_database(user_url_slug):
        flask.abort(404)

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT fullname FROM users "
        "WHERE username == ?",
        (user_url_slug, )
    )
    fullname = cur.fetchall()[0]['fullname']

    cur = connection.execute(
        "SELECT postid, filename FROM posts "
        "WHERE owner == ?",
        (user_url_slug, )
    )
    posts = cur.fetchall()

    # Add database info to context
    context = {"logname": logname, "username": user_url_slug,
               "logname_follows_username": follows(logname, user_url_slug),
               "fullname": fullname, "current_url": flask.request.path,
               "following": len(get_following_list(user_url_slug)),
               "followers": len(get_followers_list(user_url_slug)),
               "total_posts": len(posts), "posts": posts}
    return flask.render_template("user.html", **context)


@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    if not user_exists_in_database(user_url_slug):
        flask.abort(404)

    followers_list = get_followers_list(user_url_slug)
    followers = []
    for follower in followers_list:
        dic = {'username': follower, 'user_img_url': get_profile_pic(follower),
               'logname_follows_username': follows(logname, follower)}
        followers.append(dic)

    context = {"logname": logname, "followers": followers,
               "current_url": flask.request.path}
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    if not user_exists_in_database(user_url_slug):
        flask.abort(404)

    following_list = get_following_list(user_url_slug)
    following = []
    for follow in following_list:
        dic = {'username': follow, 'user_img_url': get_profile_pic(follow),
               'logname_follows_username': follows(logname, follow)}
        following.append(dic)

    context = {"logname": logname, "following": following,
               "current_url": flask.request.path}
    return flask.render_template("following.html", **context)


@insta485.app.route('/following/', methods=['POST'])
def edit_follow():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    operation = flask.request.values.get('operation')
    username = flask.request.values.get('username')
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 == ? AND username2 == ?",
        (logname, username, )
    )
    content = cur.fetchall()
    if len(content) == 0 and operation == 'unfollow':
        flask.abort(409)
    if len(content) == 1 and operation == 'follow':
        flask.abort(409)

    if operation == 'follow':
        connection.execute(
            "INSERT INTO following(username1, username2)"
            "VALUES (?, ?)",
            (logname, username, )
        )
    elif operation == 'unfollow':
        connection.execute(
            "DELETE FROM following "
            "WHERE username1 == ? AND username2 == ?",
            (logname, username, )
        )

    if flask.request.args.get('target'):
        return flask.redirect(flask.request.args.get('target'))
    return flask.redirect(flask.url_for('show_index'))
