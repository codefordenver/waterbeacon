import React, { Component, useState } from 'react';
import PageNavHeader from '../components/PageNavHeader';
import { Form, Row, Col, Button } from 'react-bootstrap';
import SubscribeForm from './SubscribeForm';

class Subscribe extends Component {

  render() {
    return (
      <div className="bg-white">
        <PageNavHeader />
        <Row className="bg-white justify-content-center">
         <Col md={4}>
            <p style={{ color: '#17a6ff'}}>Subscribe and recieve updates from our Water Beacon notifier. If there is any water quality related issues reported in your neighborhood on Twitter or by the EPA, we will let you know.</p>
            <SubscribeForm />
          </Col>
        </Row>
      </div>
    );
  }
}

export default Subscribe;
