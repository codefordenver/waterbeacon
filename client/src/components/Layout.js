import React from "react";

import { SearchBar } from "./common";
import Navbar from "./Navbar";
import Map from "./Map";
import RankList from "./RankList";
import Footer from "./Footer";

import "./Layout.css";

const Layout = () => (
  <div className="main">
    <Navbar />
    <div className="content">
      <div className="content-inner">
        <SearchBar className="main-search-bar" />
        <Map className="main-map-wrapper" />
        <RankList className="main-rank-list" />
      </div>
    </div>
    <Footer />
  </div>
);

export default Layout;
