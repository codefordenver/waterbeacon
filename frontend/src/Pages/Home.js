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

const Home = () => (
  <div className="bg-white">
    <PageNavHeader />
    <Retrieve />
    <WhyWB />
    <OpenData />
    <WorkShop />
    <Subscribe />
    <Partners />
  </div>
);

export default Home;
