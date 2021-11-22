import React from 'react';
import { Image, Col, Row, Container } from 'react-bootstrap';
import workshop from '../images/workshop.jpg'
import stickyNotes from '../images/sticky-notes.jpg'
import './WorkShop.css';

export default function WorkShop() {
  return (
    <article id="workshop" className="reverse-flex">
    <Container>
      <Row >
        <Col >
          <h1>Workshop</h1>
          <p class="text-muted">We organize workshops to inform you the basics of water quality and how you can navigate the wealth of data and find meaningful revelations about the state of water quality where you live. We also discuss with you how we can make this vision a reality. Click to subscribe to our mailing to be notified of our next workshop.</p>
        </Col>
        <Col>
          <Row>
            <Image height={ 350 }  src={workshop} alt="Workshop"/>
          </Row>
        </Col>

      </Row>
    </Container>
    </article>
  )
}
