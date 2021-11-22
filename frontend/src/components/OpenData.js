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
          <Row>
            <Image height={ 350 } src={openData} alt="Open Data"/>
          </Row>

        </Col>

        <Col>
          <h1>Open Data</h1>
          <p className="text-muted">The vision have to start somewhere. Presently, we collect data from the EPA and Twitter and the data is segmented by every US county. The EPA data produces the visualization. Explore the visualization. Zoom in to view the water quality within your county. Twitter data is to report any notification that a county may report on safety of drinking water within your city. As time progresses, and with your support, we will work towards the data getting more specific to the neighborhood level.</p>
        </Col>

      </Row>
    </Container>
    </article>
  )
}
