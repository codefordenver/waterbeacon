import React from "react";
import { Navbar as RBNavbar } from "react-bootstrap";

import Logo from "./Logo";
import NavbarControl from "./NavbarControl";

import "./Navbar.css";

const Navbar = () => (
  <RBNavbar className="navbar-shadow">
    <RBNavbar.Brand>
      <a className="navbar-brand" href="/">
        <Logo />
      </a>
    </RBNavbar.Brand>
    <NavbarControl />
  </RBNavbar>
);

export default Navbar;
