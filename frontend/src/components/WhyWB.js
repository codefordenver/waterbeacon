import React from 'react';
import { Image } from 'react-bootstrap';
import wbInfoLogo from '../images/infoWB.png'


export default function WhyWB() {
  return (
    <article id="why-wb" className="center-all">
      <div className="center-all">
        <h2 style={{ color: 'white'}}>Why?</h2>
        <Image src={wbInfoLogo} style={{ maxHeight: 100, padding:10 }}/>
      </div>
      <div className="center-all">
        <p>
             The purpose of Water Beacon is to make drinking water quality data easy to understand.
        </p>
      </div>
    </article>
  )
}
//
