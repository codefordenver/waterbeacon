import React, { Component } from 'react';
import './App.css';
import WbHeaderBsNav from './components/WbHeaderBsNav';
import Retrieve from './components/Retrieve';
import WBHeader from './Pages/WBHeader';

class App extends Component {
  render() {
    return (
      <div className="App">
        <WBHeader />
        <WbHeaderBsNav />
        <Retrieve />
      </div>
    );
  }
}

export default App;
