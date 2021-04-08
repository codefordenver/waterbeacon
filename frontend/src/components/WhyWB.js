import React from 'react';
import { Image } from 'react-bootstrap';
import wbInfoLogo from '../images/infoWB.png'
import { NavHashLink } from 'react-router-hash-link';


export default function WhyWB() {
  return (
    <article id="why-wb" className="center-all">
      <div className="center-all">
        <h2 style={{ color: 'white'}}>Why Water Beacon?</h2>
        <Image src={wbInfoLogo} style={{ maxHeight: 100, padding:10 }}/>
      </div>
      <div className="center-all" style={{ fontSize: 18, color: 'white' }}>
        <p>Water Beacon is to fill in the knowledge gap and lack of general awareness in the public. <br />
          Making information about water quality data available to the public for easy access.
        </p>
      </div>
    </article>
  )
}
//
