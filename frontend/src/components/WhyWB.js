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
      <div className="center-all" style={{ fontSize: 18, color: 'white', width:800 }}>
        <p>Imagine opening Google Maps and there there is a Water Quality layer as assessable as air quality. You could easily view which neighborhood has high water quality vs low water quality by an index rated by 0 - 100 or which river has bad water quality. You can use this index to easily understand how safe this water is to drink that is the vision of Water Beacon to make information about water quality easy to view and consume.
        </p>
      </div>
    </article>
  )
}
//
