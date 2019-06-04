import React, { Component } from 'react';
import axios from "axios";
//mport Api from "../utils/MockApi";

class ApiData extends Component {

  constructor(props) {
    console.log("ApiData.constructor()")
    super(props)
    this.state = {
      isLoading: true,
      response: null,
      error: null
    };
  }

  componentWillMount() {
    console.log("ApiData.componentWillMount()");
    axios.get("https://private-19c08-waterbeacon.apiary-mock.com/v1/data")
    .then(resp => {
      console.log(resp.data);
      this.setState({
        isLoading: false,
        response: JSON.stringify(resp.data, 2, null),
        error: null
      })
    }).catch(function (error) {
      console.log("ERROR:" + error);
    })
    .then(function () {
      console.log("THEN?");
    // always executed
    });
  }

  componentDidUpdate() {
    console.log("ApiData.componentDidUpdate()");
    console.log(this.state.response);
  }


  render () {
    const { isLoading, response, error } = this.state;
    console.log("ApiData.render()");
    console.log("ApiData.render() isLoading: " + this.state.isLoading);
    console.log("ApiData.render() ERROR: " + this.state.error);
    console.log("ApiData.render() RESPONSE: " + this.state.response);

    return(
      <div>
        { this.state.response }
      </div>
    )

  }

}

export default ApiData;
