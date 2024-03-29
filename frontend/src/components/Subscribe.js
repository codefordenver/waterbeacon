import React from 'react';
import { Container, Col, Image, Row } from 'react-bootstrap';
import { NavHashLink } from 'react-router-hash-link';

import subscribe from '../images/water-flowing.jpg'
import './Subscribe.css';
// !import data from to display to live data points

export default function subscribeView () {
  return (
    <article id="subscribe">
      <Container>
        <Row>
          <Col>
            <Row>
              <Image src={subscribe} alt="Subscribe"/>
            </Row>
          </Col>

          <Col className="vertical-center-all">
            <h2>Subscribe</h2>
            <p className="text-muted">Join a community that believes that water quality should be easy and assessable. Receive updates on notifications of any water quality issues within your neighborhood. Get the latest news from our blog.</p>
            <NavHashLink to="/subscribe/" className="btn btn-primary">
              Subscribe
            </NavHashLink>

          </Col>

        </Row>
      </Container>
    </article>
  )
}
