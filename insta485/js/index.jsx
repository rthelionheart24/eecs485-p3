import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      next: '',
      results: [],
      hasMore: false,
    };
    this.fetchMoreData = this.fetchMoreData.bind(this);
  }

  componentDidMount() {
    fetch('/api/v1/posts/', { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          next: data.next,
          results: data.results,
          hasMore: data.next !== '',
        });
      })
      .catch((error) => console.log(error));
  }

  fetchMoreData() {
    const { next } = this.state;
    fetch(next, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => ({
          next: data.next,
          results: prevState.results.concat(data.results),
          hasMore: data.next !== '',
        }));
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { results, hasMore } = this.state;
    const feed = results.map((post) => (<Post key={String(post.postid)} url={post.url} />));

    return (
      <InfiniteScroll
        next={this.fetchMoreData}
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
        dataLength={results.length}
      >
        {feed}
      </InfiniteScroll>
    );
  }
}

export default Index;
