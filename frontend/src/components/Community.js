import React from 'react';
import { Image, Card, Button, CardDeck } from 'react-bootstrap';
import wbSRC from "../WaterBeacon.svg"
import { NavHashLink } from 'react-router-hash-link';
import workShop from '../images/workshop.jpg';
import openData from '../images/openData.jpg';
import './communityStyle.css';

export default function Community() {
  return (
    <article id="community" >
      <section>
        <h3> <Image src={wbSRC} /> Community</h3>
        <p>Scientists, software developers, educators, journalists, analysts,
          activists, lovers of open environmental data from around the
          globe working for one purpose.
        </p>
      </section>
      <CardDeck className="community-cards" lg>
        <Card>
        <Image src={openData} alt="Open Data Text Image" className="card-images"/>
        <Card.Body>
          <Card.Title>Open Data</Card.Title>
          <Card.Text>Check out Where our Data comes from</Card.Text>
          <Button href="https://www.epa.gov/waterdata/water-quality-data-wqx#portal">Go To The Sources</Button>
        </Card.Body>
      </Card>
      <Card className="community-cards">
        <Image src={workShop} className="card-images"/>
        <Card.Body>
          <Card.Title>Work Shop</Card.Title>
          <Card.Text>Let us come and teach you about Water Quatlity</Card.Text>
          <NavHashLink to="./#workshop"><Button>Find Out More</Button></NavHashLink>
          </Card.Body>
        </Card>
      </CardDeck>
    </article>
  )
}
