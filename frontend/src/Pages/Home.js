import React, { Component } from 'react';
// import WbHeaderBsNav from '../components/WbHeaderBsNav';
import Retrieve from '../components/Map/Retrieve';
import PageNavHeader from '../components/PageNavHeader';
import './styleHome.css';
import WhyWB from '../components/WhyWB';
import Data from '../components/Data';
import WorkShop from '../components/WorkShop';
import Community from '../components/Community';
import Partners from '../components/Partners';
import Foot from '../components/Footer';

class Home extends Component {
  render() {
    return (
      <div>
        <PageNavHeader />
        {/* <WbHeaderBsNav /> */}
        {/*  <Retrieve /> */}
        <WhyWB />
        <Data />
        <Community />
        <Partners />
        <Foot />
      </div>
    );
  }
}

export default Home;
