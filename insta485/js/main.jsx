import React from 'react';
import ReactDOM from 'react-dom';
import Index from './index';

// This method is only called once
ReactDOM.render(
  // Insert the post component into the DOM
  <Index />,
  // <Comment
  //   text="Example Comment"
  //   lognameOwnsThis
  //   deleteComment={() => {
  //     console.log('Comment Deleted!');
  //   }}
  // />,
  document.getElementById('reactEntry'),
);
