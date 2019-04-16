import React, { Component } from 'react';
import './App.css';
import DefaultD3 from './components/DefaultD3';
import WbHeader from './components/WbHeader';

class App extends Component {
  render() {
    return (
      <div className="App">
        <WbHeader />
        <svg width="960" height="600">
          <DefaultD3 width={960} height={600} />
        </svg>
      </div>
    );
  }
}

export default App;
