import React from 'react';
import { Card } from 'react-bootstrap';

export default function liveData () {
  return (
    <article id="live">
      <section className="live-titles" >
        <h2>
          Illuminating water quality through open data and community
        </h2>
        <h4>
          Second Quote
        </h4>
      </section>
      <section className="feat">
        <Card className="feat-data "id="feat-one">
          <Card.Body>
            <Card.Title>Location of Data</Card.Title>
            <Card.Title>Name of Facility</Card.Title>
            <Card.Text>
              Water Quality Info
            </Card.Text>
          </Card.Body>
          <Card.Footer>
            <small className="text-muted">Updated Time</small>
          </Card.Footer>
        </Card>
        <Card className="feat-data" id="feat-two">
          <Card.Body>
            <Card.Title>Location of Data</Card.Title>
            <Card.Title>Name of Facility</Card.Title>
            <Card.Text>
              Water Quality Info
            </Card.Text>
          </Card.Body>
          <Card.Footer>
            <small className="text-muted">Updated Time</small>
          </Card.Footer>
        </Card>
      </section>
    </article>
  )
}
