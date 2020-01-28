import React, { Component } from 'react';
import './App.css';
import { HashRouter as Router, Route } from 'react-router-dom';
import Home from './Pages/Home';

class App extends Component {
  render() {
    return (
      <Router>
        <Route path="/" exact component={Home}/>
      </Router>
    );
  }
}

export default App;
