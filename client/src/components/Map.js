import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

import "./Map.css";

const Map = ({ className }) => (
  <div className={classNames("map-wrapper", className)}>
    <div className="map">
      <center>map</center>
    </div>
  </div>
);

Map.propTypes = {
  className: PropTypes.string
};

Map.defaultProps = {
  className: undefined
};

export default Map;
