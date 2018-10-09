import React from "react";
import PropTypes from "prop-types";

import "./IconButton.css";

const IconButton = ({ iconClassName, onClick, tooltip }) => (
  <div className="icon-button" onClick={onClick} title={tooltip}>
    <span className={`oi ${iconClassName}`} />
  </div>
);

IconButton.propTypes = {
  iconClassName: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  tooltip: PropTypes.string
};

IconButton.defaultProps = {
  onClick: () => {},
  tooltip: undefined
};

export default IconButton;
