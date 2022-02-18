import React from 'react';
import PropTypes from 'prop-types';

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
      <button className="like-unlike-button" type="submit" onClick={handleClick}>
        {lognameLikesThis ? 'unlike' : 'like'}
      </button>
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
