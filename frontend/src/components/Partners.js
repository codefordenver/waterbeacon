import React from 'react';
import { Image, Button } from 'react-bootstrap';
import './partners.css'
import cfd from '../images/CFDlogo.png';
import cfa from '../images/CFALogo.png';
import epa from '../images/EPALogo.png';
import wbLogo from '../images/waterBeaconLogo.png';

export default function Partners() {
  return (
    <article id="partners" >
      <div id="sponsor-title-container">
        <Image src={wbLogo} style={{ height: 100, marginRight:50 }} />
        <div id="sponsors-title">
          <h3>Water Beacon</h3>
          <h3>is made possible by</h3>
        </div>
      </div>
      <div id="sponsors">
        <div>
          <Button href="https://codefordenver.org/#/" variant="light" id="CFD-btn">
            <Image className="btn-img" src={cfd} alt="Code For Denver"/>
          </Button>
          <Button href="https://www.codeforamerica.org/" variant="light" id="CFA-btn">
            <Image className="btn-img" src={cfa} alt="Code for America"/>
          </Button>
          <Button href="https://www.epa.gov/" variant="light" id="EPA-btn">
            <Image className="btn-img" src={epa} alt="The Environmental Protection Agency"/>
            <h2>The EPA</h2>
          </Button>
        </div>
      </div>
    </article>
  )
}
