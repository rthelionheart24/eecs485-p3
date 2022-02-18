"""REST API for comments."""
import flask
import insta485
from insta485.api.utility import authentication, InvalidUsage


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def comment():
    logname = authentication()
    data = flask.request.json
    postid = flask.request.values.get('postid')
    text = flask.request.json.get('text')
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO comments(owner, postid, text)"
        "VALUES (?, ?, ?)",
        (logname, postid, text,)
    )
    cur = connection.execute("SELECT last_insert_rowid()")
    commentid = cur.fetchall()[0]['last_insert_rowid()']
    response = {
        'commentid': commentid,
        'lognameOwnsThis': 'true',
        'owner': logname,
        'ownerShowUrl': f'/users/{logname}/',
        'text': text,
        'url': f'/api/v1/comments/{commentid}/'
    }
    return response, 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def uncomment(commentid):
    logname = authentication()

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM comments "
        "WHERE commentid == ?",
        (commentid, )
    )
    content = cur.fetchall()
    if len(content) == 0:
        raise InvalidUsage("Not Found", 404)
    if content[0]['owner'] != logname:
        raise InvalidUsage("Forbidden", 403)

    connection.execute(
        "DELETE FROM comments "
        "WHERE commentid == ?",
        (commentid,)
    )
    return flask.Response(status=204)
