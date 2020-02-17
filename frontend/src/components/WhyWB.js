import React from 'react';
import { Container, Image } from 'react-bootstrap';
import wbInfoLogo from '../images /SMWaterBeaconInfo.png'


export default function WhyWB() {
  return (
    <article id="why-wb">
      <Image src={wbInfoLogo}/>
      <h1>Why WB</h1>
    </article>
  )
}
