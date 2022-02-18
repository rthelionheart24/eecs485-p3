import React from 'react';
import PropTypes from 'prop-types';
import DeleteCommentButton from './DeleteCommentButton';

function Comment(props) {
  const { text, lognameOwnsThis, deleteComment } = props;
  const renderCommentButton = () => {
    if (lognameOwnsThis) {
      return <DeleteCommentButton deleteComment={deleteComment} />;
    }
    return null;
  };

  return (
    <div>
      <p>{text}</p>
      {renderCommentButton()}
    </div>
  );
}

Comment.propTypes = {
  text: PropTypes.string.isRequired,
  lognameOwnsThis: PropTypes.bool.isRequired,
  deleteComment: PropTypes.func.isRequired,
};

export default Comment;
