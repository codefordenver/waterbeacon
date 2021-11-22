import React, { Component } from 'react';
// import WbHeaderBsNav from '../components/WbHeaderBsNav';
import Retrieve from '../components/Map/Retrieve';
import PageNavHeader from '../components/PageNavHeader';
import OpenData from '../components/OpenData';
import './styleHome.css';
import Subscribe from '../components/Subscribe';
import WhyWB from '../components/WhyWB';
import WorkShop from '../components/WorkShop';
import Partners from '../components/Partners';
import Directions from '../components/Directions';
import Community from '../components/Community';
import Foot from '../components/Footer';

class Home extends Component {
  render() {
    return (
      <div>
        <PageNavHeader />
        {/* <WbHeaderBsNav /> */}
        <Retrieve />
        <WhyWB />
        <OpenData />
        <WorkShop />
        <Subscribe />
        <Partners />
      </div>
    );
  }
}

export default Home;
