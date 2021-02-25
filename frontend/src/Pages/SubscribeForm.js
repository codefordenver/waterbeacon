import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const SubscribeForm = () => {
  const initialFormData = Object.freeze({
    email: "",
    zipcode: "",
    include_newsletter: "",
    include_workshop:""
  });

  const [formData, updateFormData] = React.useState(initialFormData);



  const handleChange = (e) => {
      updateFormData({
        ...formData,

        // Trimming any whitespace
        [e.target.name]: e.target.value.trim()
      });
    };

  const validEmailRegex = RegExp(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i);

  const handleSubmit = async (event) => {

    event.preventDefault();
    console.log('email', validEmailRegex.test(formData.email))
    console.log(formData)
  }

    return (
      <Form className="border p-3" onSubmit={handleSubmit} onChange={handleChange}>
        <Form.Group controlId="formEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" name="email" placeholder="" />
        </Form.Group>
        <Form.Group controlId="formZipcode">
          <Form.Label>Zip Code</Form.Label>
          <Form.Control type="zipcode" name="zipcode" placeholder="" />
        </Form.Group>
        <Form.Group controlId="formNewsletterCheckbox">
          <Form.Check type="checkbox" name="include_newsletter"  label="I'm interested recieving updates from the Water Beacon newsletter." className="text-muted"/>
        </Form.Group>
        <Form.Group controlId="formWorkshopCheckbox">
          <Form.Check type="checkbox" name="include_workshop" label="I'm interested in the workshop. Send me information when it is active." className="text-muted"/>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    )

};

export default SubscribeForm;
