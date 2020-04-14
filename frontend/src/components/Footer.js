import React from 'react';
import { Image, Navbar, Nav } from 'react-bootstrap';
import wbSVG from '../WaterBeacon.svg';
import './footerStyle.css'
import { NavHashLink } from 'react-router-hash-link';

class PageNavHeader extends React.Component {
  render() {
    return (

      <section className="page-header">
        <Navbar collapseOnSelect className="nav-bar"style={{ justifyContent: 'initial' }} expand="lg" >
          <Navbar.Brand>
            <Image src={wbSVG} alt="Water Beacon Title" />
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mr-auto nav-buttons">
              <NavHashLink to="/#why-wb" className="nav-items">
                Why Water Beacon
              </NavHashLink>
              <NavHashLink to="/#workshop" className="nav-items">
                Workshop
              </NavHashLink>
              <NavHashLink to="/#community" className="nav-items">
                Community
              </NavHashLink>
              <NavHashLink to="/#partners" className="nav-items">
                Partners
              </NavHashLink>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </section>
    )
  }
}
export default PageNavHeader
