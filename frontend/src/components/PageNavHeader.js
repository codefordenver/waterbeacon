import React from 'react';
import { Image, Navbar, Nav, Button } from 'react-bootstrap';
import wbSVG from '../WaterBeacon.svg';
import wbLogo from '../images /waterBeaconLogo.png';

class PageNavHeader extends React.Component {
  render() {
    return (
      <section className="page-header">
        <Navbar bg="light"  className="nav-bar">
          <Navbar.Brand href="#home">
            <Image src={wbLogo} style={{ height: 150 }} fluid />
            <Image src={wbSVG} />
          </Navbar.Brand>
          <Nav className="mr-auto">
            <Nav.Link href="#whyWB">Why Water Beacon</Nav.Link>
            <Nav.Link href="#community">Community</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
          </Nav>
          <div>
            <Button> Get Involved</Button>
          </div>
        </Navbar>
      </section>
    )
  }
}
export default PageNavHeader
