import React from 'react';
import { Image, Navbar, Nav, Button } from 'react-bootstrap';
import wbSVG from '../WaterBeacon.svg';
import wbLogo from '../images/waterBeaconLogo.png';
import './pageNavStyle.css'
import { NavHashLink } from 'react-router-hash-link';

class PageNavHeader extends React.Component {
  render() {
    return (

      //! get involved button needs link to the page/section

      <section className="page-header shadow">
        <Navbar collapseOnSelect className="nav-bar" bg="light" style={{justifyContent: 'initial'}} expand="lg" >
          <Navbar.Brand>
            <a href="/">
              <Image src={wbLogo} style={{ maxHeight: 40, marginRight: 5 }} fluid alt="Water Beacon Logo picture"/>
            </a>
            <a href="/">
              <Image src={wbSVG} style={{ maxHeight: 40, paddingTop: 2 }} alt="Water Beacon Title"/>
            </a>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mr-auto nav-buttons">
              <NavHashLink to="/#why-wb" className="nav-items">
                Why Water Beacon
              </NavHashLink>
              <NavHashLink to="/#opendata" className="nav-items">
                Open Data
              </NavHashLink>
              <NavHashLink to="/#workshop" className="nav-items">
                Workshop
              </NavHashLink>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <div style={{ padding: 20 }}>
          <NavHashLink to="/subscribe/" className="btn btn-primary">
            Subscribe
          </NavHashLink>
        </div>
      </section>
    )
  }
}
export default PageNavHeader
