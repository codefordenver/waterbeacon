import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

import "./Footer.css";

const Footer = ({ className }) => (
  <footer className={classNames("footer", "container-fluid", className)}>
    <div className="row footer-inner">
      <div className="col-md">&copy; 2018 WaterBeacon</div>
      <div className="col-md">
        <a className="newsletter-anchor" href="#">
          <span className="oi oi-envelope-closed" />
          <span>Sign Up For Our Newsletter!</span>
        </a>
      </div>
    </div>
  </footer>
);

Footer.propTypes = {
  className: PropTypes.string
};

Footer.defaultProps = {
  className: undefined
};

export default Footer;
