"""REST API for posts."""
import flask
import insta485
from insta485.api.utility import authentication, InvalidUsage
from insta485.views.utility import get_profile_pic, get_following_list


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post_by_id(postid_url_slug):
    """Return post on postid.

    Example:
    {
      "created": "2017-09-28 04:33:28",
      "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "ownerShowUrl": "/users/awdeorio/",
      "postShowUrl": "/posts/1/",
      "url": "/api/v1/posts/1/"
    }
    """
    logname = authentication()
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM posts WHERE postid == ?", (postid_url_slug,)
    )
    post = cur.fetchall()
    if len(post) == 0:
        raise InvalidUsage("Not Found", 404)
    post = post[0]

    cur = connection.execute(
        "SELECT * FROM comments "
        "WHERE postid == ?",
        (postid_url_slug,)
    )
    data = cur.fetchall()
    comments = []
    for d in data:
        comments.append({
            "commentid": d['commentid'],
            "lognameOwnsThis": d['owner'] == logname,
            "owner": d['owner'],
            "ownerShowUrl": f"/users/{d['owner']}/",
            "text": d['text'],
            "url": f"/api/v1/comments/{d['commentid']}/"
        })

    cur = connection.execute(
        "SELECT owner, likeid FROM likes "
        "WHERE postid == ?",
        (postid_url_slug,)
    )
    liked_users = cur.fetchall()
    numLikes = len(liked_users)
    lognameLikesThis = False
    url = None
    for d in liked_users:
        if d['owner'] == logname:
            lognameLikesThis = True
            url = f"/api/v1/likes/{d['likeid']}/"

    context = {
        "comments": comments,
        "created": post['created'],
        "imgUrl": f"/uploads/{post['filename']}",
        "likes": {
            "lognameLikesThis": lognameLikesThis,
            "numLikes": numLikes,
            "url": url
        },
        "owner": f"{post['owner']}",
        "ownerImgUrl": f"/uploads/{get_profile_pic(post['owner'])}",
        "ownerShowUrl": f"/users/{post['owner']}/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/')
def get_posts_by_args():
    logname = authentication()
    following_list = get_following_list(logname)
    following_list.append(logname)
    connection = insta485.model.get_db()
    if len(following_list) == 1:
        cur = connection.execute(
            "SELECT * FROM posts "
            "WHERE owner == ?",
            (logname, )
        )
    else:
        cur = connection.execute(
            f"SELECT * FROM posts "
            f"WHERE owner IN {tuple(following_list)} "
        )
    posts = cur.fetchall()

    size = flask.request.args.get('size', default=10, type=int)
    page = flask.request.args.get('page', default=0, type=int)
    postid_lte = flask.request.args.get('postid_lte',
                                        default=posts[-1]['postid'], type=int)
    if size < 0 or page < 0:
        raise InvalidUsage("Bad Request", 400)
    next_page_url = f"/api/v1/posts/?size={size}&page" \
                    f"={page + 1}&postid_lte={postid_lte}"
    start = size * page
    end = min(postid_lte, size * (page + 1))

    posts = [post for post in posts if post['postid'] <= postid_lte]
    query_string = flask.request.query_string.decode('utf-8')
    query_string = f"?{query_string}" if query_string else ""
    current_url = f"{flask.request.path}{query_string}"
    results = [{"postid": post['postid'],
                "url": f"/api/v1/posts/{post['postid']}/"}
               for i, post in enumerate(reversed(posts)) if start <= i < end]

    next_page_url = "" if len(results) < size else next_page_url
    context = {
        "next": next_page_url,
        "results": results,
        "url": current_url
    }
    return context
