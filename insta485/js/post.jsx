import React from 'react';
import PropTypes from 'prop-types';

class Post extends React.Component {
  /* Display number of image and post owner of a single post
  */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      imgUrl: '',
      owner: '',
      ownerImgUrl: '',
      ownerShowUrl: '',
      postShowUrl: '',
      postid: '',
      url: '',
      comments: '',
      created: '',
      likes: '',
    };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          imgUrl: data.imgUrl,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          postShowUrl: data.postShowUrl,
          postid: data.postid,
          url: data.url,
          comments: data.comments,
          created: data.created,
          likes: data.likes,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const {
      imgUrl, owner, ownerImgUrl, ownerShowUrl, postShowUrl, postid, url, comments, created, likes,
    } = this.state;

    // Render number of post image and post owner
    return (
      <div className="post">
        <div className="row-container">
          <img src={`/uploads/${ownerImgUrl}/`} alt="" style="width: 30px; height: 30px; margin-top: 15px; margin-left: 15px;"/>
          <a href={`/users/${owner}/`} className="child" style="width: 37.5%;">{owner}</a>
          <a href={`/posts/${postid}/`} className="child" style="text-align: end; color: grey">{{ created }}</a>
        </div>

        <div>
          <img src={`/uploads/${imgUrl}/`} alt="">
            if (likes == 1)
              <p class="child">1 like</p>
            else
              <p class="child">{likes} likes</p>

            {% for comment in post.comments %}
            <div class="comment">
              <a href={`/users/${comment.owner}/`}>{ comment.owner }</a> {{ comment.text }}
              {% if logname == comment.owner %}
              {/*<!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') -->*/}
              <form action={`/comments/?target=${ current_url }`} method="post" enctype="multipart/form-data">
                <input type="hidden" name="operation" value="delete" />
                <input type="hidden" name="commentid" value="{{ comment.commentid }}" />
                <input type="submit" name="uncomment" value="delete" />
              </form>
              {% endif %}
            </div>
            {% endfor %}
            {% if liked == true %}
            {/*<!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') -->*/}
            <form class="form" action={`${url_for('edit_likes')}?target={ current_url }`} method="post" enctype="multipart/form-data">
              <input type="hidden" name="operation" value="unlike" />
              <input type="hidden" name="postid" value="{ post.postid }" />
              <input type="submit" name="unlike" value="unlike" />
            </form>
            {% else %}
            {/*<!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') -->*/}
            <form class="form" action={`/likes/?target=${current_url}`} method="post" enctype="multipart/form-data">
              <input type="hidden" name="operation" value="like" />
              <input type="hidden" name="postid" value="{ post.postid }" />
              <input type="submit" name="like" value="like" />
            </form>
            {% endif %}
            {/*<!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') -->*/}
            <form class="form" action={`/comments/?target=${current_url}`} method="post" enctype="multipart/form-data">
              <input type="hidden" name="operation" value="create" />
              <input type="hidden" name="postid" value="{{ post.postid }}" />
              <input type="text" name="text" required />
              <input type="submit" name="comment" value="comment" />
            </form>
            {% if logname == post.owner %}
            {/*<!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') -->*/}
            <form class="form" action={`/posts/?target=${logged_in_user_url}`} method="post" enctype="multipart/form-data">
              <input type="hidden" name="operation" value="delete" />
              <input type="hidden" name="postid" value="{{ post.postid }}" />
              <input type="submit" name="delete" value="delete this post" />
            </form>
            {% endif %}
        </div>


      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
