import React, { Component } from 'react';
import WbHeaderBsNav from '../components/WbHeaderBsNav';
import Retrieve from '../components/Retrieve';
import PageNavHeader from '../components/PageNavHeader';
import LiveData from '../components/LiveData';
import './styleHome.css';
import WhyWB from '../components/WhyWB';

class Home extends Component {
  render() {
    return (
      <div>
        <PageNavHeader />
        {/* <WbHeaderBsNav />
        <Retrieve /> */}
        <LiveData />
        <WhyWB />
      </div>
    );
  }
}

export default Home;



