import React from 'react';
import PropTypes from 'prop-types';

export default class LikeUnlikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { logname: '', postid: '' };
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    const { logname, postid } = this.props;
    this
  }

  render() {
    const { liked } = this.state;
    const buttonText = liked ? 'like' : 'unlike';
    return (
      <button type="button" className="like-unlike-button">
        $
        {buttonText}
      </button>
    );
  }
}

LikeUnlikeButton.propTypes = {
  liked: PropTypes.string.isRequired,
  postid: PropTypes.number.isRequired,
};
