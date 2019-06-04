import React, { Component } from 'react';
import './App.css';
import DefaultD3 from './components/DefaultD3';
import WbHeader from './components/WbHeader';
import WbHeaderBsNav from './components/WbHeaderBsNav';
import ApiData from './components/ApiData';

class App extends Component {
  render() {
    return (
      <div className="App">
        <WbHeaderBsNav />
        <svg width="960" height="600">
          <DefaultD3 width={960} height={600} />
        </svg>
        <ApiData />
      </div>
    );
  }
}

export default App;
