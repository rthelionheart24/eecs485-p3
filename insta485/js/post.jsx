import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Comment from './comment';
import Likes from './likes';
import CommentForm from './commentForm';

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
      comments: [{
        commentid: 0,
        lognameOwnsThis: false,
        owner: '',
        ownerShowUrl: '',
        text: '',
        url: '',
      }],
      created: '',
      likes: {
        lognameLikesThis: false,
        numLikes: 0,
        url: '',
      },
    };
    this.deleteComment = this.deleteComment.bind(this);
    this.submitComment = this.submitComment.bind(this);
    this.like = this.like.bind(this);
    this.unlike = this.unlike.bind(this);
    this.doubleClick = this.doubleClick.bind(this);
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
          comments: data.comments,
          created: data.created,
          likes: data.likes,
        });
      })
      .catch((error) => console.log(error));
  }

  submitComment(commentText) {
    const { comments, postid } = this.state;
    const url = `/api/v1/comments/?postid=${postid}`;
    fetch(url, {
      credentials: 'same-origin',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: commentText }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((comment) => {
        this.setState({ comments: comments.concat(comment) });
      })
      .catch((error) => console.log(error));
  }

  deleteComment(url) {
    const { comments } = this.state;
    fetch(url, { credentials: 'same-origin', method: 'DELETE' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .catch((error) => console.log(error));
    this.setState(
      { comments: comments.filter((comment) => comment.url !== url) },
    );
  }

  like() {
    const { postid } = this.state;
    const url = `/api/v1/likes/?postid=${postid}`;
    fetch(url, {
      credentials: 'same-origin',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((like) => {
        this.setState((prevState) => ({
          likes: {
            lognameLikesThis: true,
            numLikes: prevState.likes.numLikes + 1,
            url: like.url,
          },
        }));
      })
      .catch((error) => console.log(error));
  }

  unlike() {
    const { likes } = this.state;
    fetch(likes.url, { credentials: 'same-origin', method: 'DELETE' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        this.setState((prevState) => ({
          likes: {
            lognameLikesThis: false,
            numLikes: prevState.likes.numLikes - 1,
            url: null,
          },
        }));
      })
      .catch((error) => console.log(error));
  }

  doubleClick() {
    const { likes } = this.state;
    if (!likes.lognameLikesThis) {
      this.like();
    }
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const {
      imgUrl,
      owner,
      ownerImgUrl,
      ownerShowUrl,
      postShowUrl,
      comments,
      created,
      likes,
    } = this.state;
    const timestamp = moment.utc(created).fromNow();

    const renderComments = () => comments.map((comment) => (
      <div key={String(comment.commentid)}>
        <Comment
          className="comment"
          url={comment.url}
          owner={comment.owner}
          text={comment.text}
          lognameOwnsThis={comment.lognameOwnsThis}
          deleteComment={this.deleteComment}
        />
      </div>
    ));

    // Render number of post image and post owner
    return (
      <div className="post">
        <div className="row-container">
          <a href={ownerShowUrl}>
            <img src={ownerImgUrl} className="profile-picture" alt="" />
          </a>
          <a href={ownerShowUrl} className="username">{ owner }</a>
          <a href={postShowUrl} className="timestamp">{ timestamp }</a>
        </div>
        <img src={imgUrl} className="post-image" onDoubleClick={this.doubleClick} alt="" />
        <Likes
          numLikes={likes.numLikes}
          lognameLikesThis={likes.lognameLikesThis}
          like={this.like}
          unlike={this.unlike}
        />
        {renderComments()}
        <CommentForm submitComment={this.submitComment} />
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
