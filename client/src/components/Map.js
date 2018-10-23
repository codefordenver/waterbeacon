import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

import { LoadingIndicator } from './common';
import { HttpWrapper } from './wrappers';

import "./Map.css";

const Map = ({ className }) => (
  <HttpWrapper
    render={({ data, isLoading }) => {
      console.log(data);
      if (isLoading) {
        return <LoadingIndicator />;
      }
      return (
        <div className={classNames("map-wrapper", className)}>
          <div className="map">
            <center>map</center>
          </div>
        </div>
      )
    }}
  />
);

Map.propTypes = {
  className: PropTypes.string
};

Map.defaultProps = {
  className: undefined
};

export default Map;
