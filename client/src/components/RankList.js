import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

import { ListGroup } from "./common";

import "./RankList.css";

const RankList = ({ className, data }) => (
  <div className={classNames("rank-list", className)}>
    <h4 className="rank-list-header">City Rankings</h4>
    <ListGroup
      alternating={true}
      data={data}
      numbered={true}
      listItemProps={{ as: "a", href: (d, i) => "#" }}
    />
  </div>
);

RankList.propTypes = {
  className: PropTypes.string,
  data: PropTypes.arrayOf(PropTypes.string)
};

RankList.defaultProps = {
  className: undefined,
  //data: []
  data: [
    "Denver, CO",
    "New York, NY",
    "Seattle, WA",
    "Portland, OR",
    "Charlotte, NC",
    "Boston, MA",
    "Burlington, VT",
    "Omaha, NE",
    "New Orleans, LA",
    "San Antonio, TX"
  ]
};

export default RankList;
