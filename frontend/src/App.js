import React, { Component } from 'react';
import './App.css';
import WbHeaderBsNav from './components/WbHeaderBsNav';
import Retrieve from './components/Retrieve';

class App extends Component {
  render() {
    return (
      <div className="App">
        <WbHeaderBsNav />
        <Retrieve />
      </div>
    );
  }
}

export default App;
