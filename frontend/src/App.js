import React, { Component } from 'react';
import './App.css';
import DefaultD3 from './components/DefaultD3';
import WbHeaderBsNav from './components/WbHeaderBsNav';

class App extends Component {
  render() {
    return (
      <div className="App">
        <WbHeaderBsNav />
        <DefaultD3/>
      </div>
    );
  }
}

export default App;
