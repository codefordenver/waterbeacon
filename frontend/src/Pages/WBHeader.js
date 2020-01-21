import React from 'react';
import { Image, Navbar, Nav } from 'react-bootstrap';


class WBHeader extends React.Component {
  render() {
    return (
      <article>
        <section>
        <Image> </Image>
        <h1 classname="display-1">Water Beacon</h1>
          <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="#home">Navbar</Navbar.Brand>
            <Nav className="mr-auto">
              <Nav.Link href="#whyWB">Why Water Beacon</Nav.Link>
              <Nav.Link href="#community">Community</Nav.Link>
              <Nav.Link href="#about">About</Nav.Link>
            </Nav>
          </Navbar>
        </section>
      </article>
    )
  }
}

export default WBHeader;