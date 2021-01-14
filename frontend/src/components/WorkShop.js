import React from 'react';
import { Image, Col, Row, Container } from 'react-bootstrap';
import workshop from '../images/workshop.jpg'
import stickyNotes from '../images/sticky-notes.jpg'
import './WorkShop.css';

export default function WorkShop() {
  return (
    <article id="workshop" className="reverse-flex">
    <Container>
      <Row>
        <Col>

        </Col>
        <Col>
          <h1>Workshop</h1>
          <p class="text-muted">Our goal is to organize workshops. In the workshop, we will teach you the basics of water quality and how you
          can navigate the wealth of data to find meaningful insights. Click to subscribe to our maillist find out about our
          next workshop. </p>
        </Col>
      </Row>
    </Container>
    </article>
  )
}
