import React from 'react';
import { Card, Container, Col, Image, Row } from 'react-bootstrap';
import epaLogo from '../images/EPALogo.png'
import ewgLogo from '../images/ewg-logo.gif'
import twitterLogo from '../images/twitter-logo.jpg'
import openData from '../images/openData.jpg'
import './OpenData.css';
// !import data from to display to live data points

export default function liveData () {
  return (
    <article id="opendata">
    <Container>
      <Row>
        <Col>
          <h1>Open Data</h1>
          <p class="text-muted">We capture data from multiple platforms including the EPA used for sourcing the map, Twitter used for notifications.</p>
        </Col>
        <Col>
          <Row>
            <Image height={ 350 } src={openData} alt="Open Data"/>
          </Row>

        </Col>
      </Row>
    </Container>
    </article>
  )
}
