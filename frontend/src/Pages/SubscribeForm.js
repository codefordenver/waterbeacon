import axios from 'axios'
import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const SubscribeForm = () => {
  const initialFormData = Object.freeze({
    email: "",
    zipcode: "",
    newsletter: "",
    workshop:""
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

  const getCookie = (name) => {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  const handleSubmit = async (event) => {


    event.preventDefault();
    if ( validEmailRegex.test(formData.email) ) {
      var csrftoken = getCookie('csrftoken');

      // create account
      var endpoint = '/v1/subscribe/'
      axios.post(endpoint,{
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        }, {
        'email': formData.email,
        'newsletter': ( formData.newsletter == 'on') ? true : false,
        'workshop': ( formData.workshop == 'on') ? true : false,
        'zipcode': formData.zipcode
      }})
      .then( response => {
        // return to homepage and post notification

      })

    }


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
          <Form.Check type="checkbox" name="newsletter"  label="I'm interested recieving updates from the Water Beacon newsletter." className="text-muted"/>
        </Form.Group>
        <Form.Group controlId="formWorkshopCheckbox">
          <Form.Check type="checkbox" name="workshop" label="I'm interested in the workshop. Send me information when it is active." className="text-muted"/>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    )

};

export default SubscribeForm;
