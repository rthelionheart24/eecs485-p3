import React from 'react';
import PropTypes from 'prop-types';

function DeleteCommentButton(props) {
  const { deleteComment } = props;
  return (
    <button
      type="button"
      className="delete-comment-button"
      onClick={deleteComment}
    >
      Delete comment
    </button>
  );
}

DeleteCommentButton.propTypes = {
  deleteComment: PropTypes.func.isRequired,
};

export default DeleteCommentButton;
