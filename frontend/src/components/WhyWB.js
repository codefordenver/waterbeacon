import React from 'react';
import { Image } from 'react-bootstrap';
import wbInfoLogo from '../images/infoWB.png'
import { NavHashLink } from 'react-router-hash-link';


export default function WhyWB() {
  return (
    <article id="why-wb" className="center-all" style={{ backgroundColor:'#198CFF', color:'white', minHeight: 300}}>
        <section className="live-titles" >
        <h2>
          Illuminating water quality through open data and community
        </h2>
        <p>Water Beacon mission is to fill in the knowledge gap and lack of general awareness in the public. <br />
          Making information about water quality data available to the public for easy access.
        </p>
    </section>
    </article>
  )
}
//
