import React from 'react';
import PropTypes from 'prop-types';
import LikeUnlikeButton from './likeUnlikeButton';

export default function Likes(props) {
  const {
    like, unlike, lognameLikesThis, numLikes,
  } = props;
  const handleClick = () => {
    if (lognameLikesThis) {
      unlike();
    } else {
      like();
    }
  };

  return (
    <div>
      <LikeUnlikeButton handleClick={handleClick} lognameLikesThis={lognameLikesThis} />
      <p className="likesDisplay">
        {numLikes}
        {' '}
        {numLikes === 1 ? 'like' : 'likes'}
      </p>
    </div>
  );
}

Likes.propTypes = {
  like: PropTypes.func.isRequired,
  unlike: PropTypes.func.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
  numLikes: PropTypes.number.isRequired,
};
