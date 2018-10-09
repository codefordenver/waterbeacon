import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import { ListGroup as RBListGroup, ListGroupItem } from "react-bootstrap";

import NumberedListGroupItem from "./NumberedListGroupItem";

import "./ListGroup.css";

class ListGroup extends RBListGroup {
  render() {
    const listGroupPropTypeNames = Object.keys(ListGroup.propTypes);

    const rbListGroupPropTypeNames = Object.keys(RBListGroup.propTypes).filter(
      key => !listGroupPropTypeNames.includes(key)
    );

    const listGroupProps = {};
    const rbListGroupProps = {};

    Object.keys(this.props).forEach(key => {
      const { [key]: propValue } = this.props;

      if (rbListGroupPropTypeNames.includes(key)) {
        rbListGroupProps[key] = propValue;
      } else {
        listGroupProps[key] = propValue;
      }
    });

    const {
      alternating,
      children,
      className,
      data,
      listItemProps,
      numbered
    } = listGroupProps;

    const customChildren =
      children ||
      data.map((d, i) => {
        const commonProps = {
          key: i,
          children: d,
          className: classNames({ alternating }),
          ...listItemProps
        };
        if (numbered) {
          return <NumberedListGroupItem number={i + 1} {...commonProps} />;
        }
        return <ListGroupItem {...commonProps} />;
      });

    return (
      <div
        className={classNames("list-group-wrapper", { alternating, className })}
      >
        {super.render.call({
          ...this,
          props: {
            ...rbListGroupProps,
            children: customChildren,
            className: "list-group"
          }
        })}
      </div>
    );
  }
}

ListGroup.propTypes = {
  alternating: PropTypes.bool,
  children: PropTypes.oneOfType([
    PropTypes.node,
    PropTypes.arrayOf(PropTypes.node)
  ]),
  className: PropTypes.string,
  data: PropTypes.arrayOf(PropTypes.any),
  listItemProps: PropTypes.shape({}),
  numbered: PropTypes.bool
};

ListGroup.defaultProps = {
  alternating: false,
  children: undefined,
  className: undefined,
  data: [],
  listItemProps: {},
  numbered: false
};

export default ListGroup;
