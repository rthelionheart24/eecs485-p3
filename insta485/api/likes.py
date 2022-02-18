"""REST API for likes."""
import flask
import insta485
from insta485.api.utility import authentication, InvalidUsage


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def like():
    logname = authentication()

    postid = flask.request.values.get('postid')
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM likes "
        "WHERE owner == ? AND postid == ?",
        (logname, postid, )
    )
    content = cur.fetchall()
    if len(content) == 1:
        likeid = content[0]['likeid']
        endpoint = f'/api/v1/likes/{likeid}/'
        response = {'likeid': likeid, 'url': endpoint}
        return response, 200
    connection.execute(
        "INSERT INTO likes(owner, postid)"
        "VALUES (?, ?)",
        (logname, postid,)
    )
    cur = connection.execute("SELECT last_insert_rowid()")
    likeid = cur.fetchall()[0]['last_insert_rowid()']
    endpoint = f'/api/v1/likes/{likeid}/'
    response = {'likeid': likeid, 'url': endpoint}
    return response, 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def unlike(likeid):
    logname = authentication()

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM likes "
        "WHERE likeid == ?",
        (likeid, )
    )
    content = cur.fetchall()
    if len(content) == 0:
        raise InvalidUsage("Not Found", 404)
    if content[0]['owner'] != logname:
        raise InvalidUsage("Forbidden", 403)

    connection.execute(
        "DELETE FROM likes "
        "WHERE likeid == ?",
        (likeid,)
    )
    return flask.Response(status=204)
