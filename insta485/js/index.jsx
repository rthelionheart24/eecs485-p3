import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';

class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      next: '',
      results: [],
      url: '',
    };
  }

  componentDidMount() {
    fetch('api/v1/posts/', { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          next: data.next,
          results: data.results,
          url: data.url,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { next, results, url } = this.state;
    const feed = results.map((post) => (<Post url={post.url} />));

    return (
      <div>
        {feed}
      </div>
    );
  }
}

export default Index;
