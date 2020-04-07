import React from 'react';
import { Image } from 'react-bootstrap';
import wbInfoLogo from '../images/infoWB.png'
import { NavHashLink } from 'react-router-hash-link';


export default function WhyWB() {
  return (
    <article id="why-wb" className="center-all">
      <div className="center-all">
        <h1>Why Water Beacon?</h1>
        <Image src={wbInfoLogo}/>
      </div>
      <div className="center-all">
        <p>Water Beacon is to fill in the knowledge gap and lack of general awareness in the public. <br />
          Making information about water quality data available to the public for easy access.
        </p>
        <p>For more in depth information check out our <NavHashLink to="/#workshop">Water Beacon Seminar</NavHashLink> below.</p>
      </div>
    </article>
  )
}
//  