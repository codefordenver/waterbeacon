import React from 'react';
import { Image, Navbar, Nav, Button } from 'react-bootstrap';
import wbSVG from '../WaterBeacon.svg';
import wbLogo from '../images /waterBeaconLogo.png';
import "./HeaderNav.css"

class PageNavHeader extends React.Component {
  render() {
    return (
      //! need header to expand across whole page and mobile version of header to work...
      <section className="page-header">
        <Navbar className="nav-bar" bg="light" fill expand="lg" >
          <Navbar.Brand href="#home">
            <Image src={wbLogo} style={{ maxHeight: 150 }} fluid />
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
