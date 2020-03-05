import React from 'react';
import { Image, Card } from 'react-bootstrap';
import Accordion from 'react-bootstrap/Accordion'
import wbInfoLogo from '../images/SMWaterBeaconInfo.png';
import './AccordionDirections.css';

export default function Directions() {
  return (
    
    <article id="directions">
      <Accordion>
        <Card>
          <Card.Header id="directions-clickable" className="background-off-white">
            <Accordion.Toggle as={Card.Header} variant="link" eventKey="1">
              <Image src={wbInfoLogo} alt="Directions click here"/> 
              Need Help?
            </Accordion.Toggle>
          </Card.Header>
          <Accordion.Collapse eventKey="1">
            <Card.Body className="background-off-white">
              Either click on the map or use the search bar to look for your areas <br />
              to see your local water resources plants compliance.
            </Card.Body> 
          </Accordion.Collapse>
        </Card>
      </Accordion>
    </article>
  )
}

