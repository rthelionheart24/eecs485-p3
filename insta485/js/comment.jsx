import React from 'react';
import PropTypes from 'prop-types';
import DeleteCommentButton from './deleteCommentButton';

function Comment(props) {
  const {
    url, text, owner, lognameOwnsThis, deleteComment,
  } = props;
  const deleteCommentHandler = () => {
    deleteComment(url);
  };
  const renderCommentButton = () => {
    if (lognameOwnsThis) {
      return <DeleteCommentButton deleteComment={deleteCommentHandler} />;
    }
    return null;
  };

  return (
    <div className="comment">
      <div className="comment-text">
        <a href={`/users/${owner}/`}>{owner}</a>
        <p>{text}</p>
      </div>
      {renderCommentButton()}
    </div>
  );
}

Comment.propTypes = {
  url: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  lognameOwnsThis: PropTypes.bool.isRequired,
  deleteComment: PropTypes.func.isRequired,
};

export default Comment;
