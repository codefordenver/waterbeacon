import React, { Component } from 'react';

class WbHeader extends Component {
  render() {
    return (
      //NEED TO FIGURE OUT HOW TO USE BOOTSTRAP WITH REACT COMPONENTS
      <header>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <h4 className="my-0 font-weight-normal" style={{color:"#17a6ff", fontSize: "25px"}}>Water&nbsp;</h4>
          <h4 className="my-0 font-weight-normal" style={{color:"#1a4e6e", fontSize: "25px"}}>Beacon</h4>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
            </ul>
            <form class="form-inline my-2 my-lg-0">
              <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
              <button className="btn btn-outline-secondary my-2 my-sm-0" type="submit">Search</button>
            </form>
          </div>
        </nav>
      </header>
    );
  }
}

export default WbHeader;
