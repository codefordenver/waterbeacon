import React, { Component } from 'react';
import './App.css';
import DefaultD3 from './components/DefaultD3';

class App extends Component {
  render() {
    return (

      <div className="App">

        <header className="App-header">
          <DefaultD3/>
        </header>
      </div>
    );
  }
}

export default App;
