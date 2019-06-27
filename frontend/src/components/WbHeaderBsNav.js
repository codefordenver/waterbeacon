import React, { Component } from 'react';
import wbLogo from "../WaterBeacon.svg";

class WbHeader extends Component {
  render() {
    return (
      <header>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <a className="navbar-brand" href="#">
            <img src={wbLogo} alt=""/>
          </a>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
            </ul>
            <form className="form-inline my-2 my-lg-0">
              <button className="btn btn-outline-secondary my-2 my-sm-0" type="submit">Subscribe</button>
            </form>
          </div>
        </nav>
      </header>
    );
  }
}

export default WbHeader;
