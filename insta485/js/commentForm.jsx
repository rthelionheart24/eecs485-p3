import React from 'react';
import PropTypes from 'prop-types';

class CommentForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };
    this.handleChange = this.handleChange.bind(this);
    this.submitComment = this.submitComment.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  submitComment(event) {
    const { submitComment } = this.props;
    const { value } = this.state;
    event.preventDefault();
    submitComment(value);
    this.setState({ value: '' });
  }

  render() {
    const { value } = this.state;
    return (
      <form className="comment-form" onSubmit={this.submitComment}>
        <input type="text" value={value} onChange={this.handleChange} />
      </form>
    );
  }
}

CommentForm.propTypes = {
  submitComment: PropTypes.func.isRequired,
};

export default CommentForm;
