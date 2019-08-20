import React, { Component } from 'react';

class WbHeader extends Component {
  render() {
    return (
      //NEED TO FIGURE OUT HOW TO USE BOOTSTRAP WITH REACT COMPONENTS
      <header>
        <div className="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm">
          <h4 className="my-0 font-weight-normal" style={{color:"#17a6ff", fontSize: "25px"}}>Water&nbsp;</h4>
          <h4 className="my-0 font-weight-normal" style={{color:"#1a4e6e", fontSize: "25px"}}>Beacon</h4>
        </div>
      </header>
    );
  }
}

export default WbHeader;
