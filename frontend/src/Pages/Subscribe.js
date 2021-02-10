import React, { Component } from 'react';
import PageNavHeader from '../components/PageNavHeader';
import { Form, Row, Col, Button } from 'react-bootstrap';

class Subscribe extends Component {

  //const [validated, setValidated] = useState(false);
  /*
  const handleSubmit = (event) => {

    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }

    setValidated(true);
  };
*/
  render() {
    return (
      <div>
        <PageNavHeader />
        <Row className="justify-content-center">
         <Col md={3}>
            <p style={{ color: '#17a6ff'}}>Subscribe and Recieve updates from our notifier if there are any water quality related issues in your neighborhood.</p>
            <Form className="border p-3" validated={validated} >
              <Form.Group controlId="formEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="" />
              </Form.Group>
              <Form.Group controlId="formZipcode">
                <Form.Label>Zip Code</Form.Label>
                <Form.Control type="zipcode" placeholder="" />
              </Form.Group>
              <Form.Group controlId="formNewsletterCheckbox">
                <Form.Check type="checkbox" label="I'm interested recieving updates from the Water Beacon Newletter." className="text-muted"/>
              </Form.Group>
              <Form.Group controlId="formWorkshopCheckbox">
                <Form.Check type="checkbox" label="I'm interested in workshop. Send me information when it is active." className="text-muted"/>
              </Form.Group>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Subscribe;
