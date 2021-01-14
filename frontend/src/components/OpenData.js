import React from 'react';
import { Card, Container, Col, Image, Row } from 'react-bootstrap';
import epaLogo from '../images/EPALogo.png'
import ewgLogo from '../images/ewg-logo.gif'
import twitterLogo from '../images/twitter-logo.jpg'
import openData from '../images/openData.jpg'
// !import data from to display to live data points

export default function liveData () {
  return (
    <article id="open-data">
    <Container>
      <Row>
        <Col>
          <h1>Open Data</h1>
          <p class="text-muted">Data collected for Water Beacon was collected using the EPA, Environmental Working Group, and Twitter.</p>
        </Col>
        <Col>
          <Row>

          </Row>

        </Col>
      </Row>
    </Container>
    </article>
  )
}
