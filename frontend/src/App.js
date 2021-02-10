import React, { Component } from 'react';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './Pages/Home';
import Subscribe from './Pages/Subscribe';

class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route path="/" exact component={Home}/>
            <Route path="/subscribe/" exact component={Subscribe}/>
        </Switch>
      </Router>
    );
  }
}

export default App;
