import React from 'react';
import { Image, Navbar, Nav, Button } from 'react-bootstrap';
import wbSVG from '../WaterBeacon.svg';
import wbLogo from '../images /waterBeaconLogo.png';
import "./HeaderNav.css"

class PageNavHeader extends React.Component {
  render() {
    return (
      //! need header for mobile version of header...
      <section className="page-header">
        <Navbar className="nav-bar" bg="light"  expand="md" >
          <Navbar.Brand href="#home">
            <Image src={wbLogo} style={{ maxHeight: 110 }} fluid />
            <Image src={wbSVG} />
          </Navbar.Brand>
          <Nav className="mr-auto nav-buttons" >
            <Nav.Link href="#why-wb">Why Water Beacon</Nav.Link>
            <Nav.Link href="#community">Community</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
          </Nav>
        </Navbar>
        <div>
          <Button> Get Involved</Button>
        </div>
      </section>
    )
  }
}
export default PageNavHeader
