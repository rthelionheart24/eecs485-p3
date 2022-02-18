import React from 'react';
import PropTypes from 'prop-types';

export default function LikeUnlikeButton(props) {
  const { handleClick, lognameLikesThis } = props;
  return (
    <button className="like-unlike-button" type="submit" onClick={handleClick}>
      {lognameLikesThis ? 'unlike' : 'like'}
    </button>
  );
}

LikeUnlikeButton.propTypes = {
  handleClick: PropTypes.func.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
};
