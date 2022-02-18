import React from 'react';
import PropTypes from 'prop-types';

function LikeUnlikeButton(props) {
  const { handleClick } = props;
  return (
    <button
      type="button"
      className="delete-comment-button"
      onClick={handleClick}
    >
      Delete comment
    </button>
  );
}

LikeUnlikeButton.propTypes = {
  handleClick: PropTypes.func.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
};
