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
              <Image src={openData} alt="Open Data"/>
            </Row>

          </Col>

          <Col className="vertical-center-all">
            <h2>Open Data</h2>
            <p>
                Using EPA data, we created a score to identify which counties have good versus bad drinking water.
                We use the score to rank each county. Counties ranked 1 have the best drinking water.
            </p>
            <p>
                Moreover, we use Twitter to identify counties that may report water quality alerts. If you subscribe and submit your zipcode, you will
                recieve a notification, if there are any water quality alerts within your county.
            </p>
          </Col>

        </Row>
      </Container>
    </article>
  )
}
