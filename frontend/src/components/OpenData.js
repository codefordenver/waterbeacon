import React from 'react';
import { Card } from 'react-bootstrap';
import { Image, ListGroup } from 'react-bootstrap';
import waterBottle from '../images/clear-glass-h2o-bottle.jpg'
// !import data from to display to live data points

export default function liveData () {
  return (
    <article id="open-data">

      <section id="shop-desc">
        <h2>Try our Water Beacon work shop</h2>
        <div>
          <h5>Find in depth answers to questions like:</h5>
          <ListGroup variant="flush">
            <ListGroup.Item>
              Where does my water come from?
            </ListGroup.Item>
            <ListGroup.Item>
              What is the history of treatment and regulation of water?
            </ListGroup.Item>
            <ListGroup.Item>
              What is the future of water quality regulations and should I be concerned?
            </ListGroup.Item>
          </ListGroup>
        </div>
      </section>
      <section id="shop-img">
        <div >
          <Image src={waterBottle} rounded/>
        </div>
      </section>
    </article>
  )
}
