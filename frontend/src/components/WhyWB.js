import React from 'react';
import { Container, Image } from 'react-bootstrap';
import wbInfoLogo from '../images /SMWaterBeaconInfo.png'


export default function WhyWB() {
  return (
    <article id="why-wb" className="center-all">
      <div className="center-all">
        <h1>Why Water Beacon</h1>
        <Image src={wbInfoLogo}/>
      </div>
      <div className="center-all">
        <h3>Spreading knowledge and awareness on water quality.</h3>
        <h3>For more information check out our Water Beacon Seminar <a>here</a></h3>
      </div>
    </article>
  )
}
