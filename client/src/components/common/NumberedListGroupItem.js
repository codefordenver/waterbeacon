import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import { ListGroupItem } from "react-bootstrap";

import "./NumberedListGroupItem.css";

class NumberedListGroupItem extends ListGroupItem {
  render() {
    const numberedListGroupItemPropNames = Object.keys(
      NumberedListGroupItem.propTypes
    );
    const listGroupItemPropNames = Object.keys(ListGroupItem.propTypes)
      .concat("children")
      .filter(key => !numberedListGroupItemPropNames.includes(key));

    const numberedListGroupItemProps = {};
    const listGroupItemProps = {};

    Object.keys(this.props).forEach(key => {
      const { [key]: propValue } = this.props;

      if (listGroupItemPropNames.includes(key)) {
        listGroupItemProps[key] = propValue;
      } else {
        numberedListGroupItemProps[key] = propValue;
      }
    });

    const {
      as: WrapperElement,
      className,
      number,
      href,
      ...props
    } = numberedListGroupItemProps;

    let customHref;
    if (typeof href === "function") {
      customHref = href(this.props.children, number - 1);
    } else if (typeof href === "string") {
      customHref = href;
    }

    return (
      <WrapperElement
        className={classNames("numbered-list-group-item", className)}
        href={customHref}
        {...props}
      >
        <div className="number-wrapper">
          <span>{number}</span>
        </div>
        {super.render.call({
          ...this,
          props: { ...listGroupItemProps, className: "list-group-item" }
        })}
      </WrapperElement>
    );
  }
}

NumberedListGroupItem.propTypes = {
  as: PropTypes.string,
  className: PropTypes.string,
  href: PropTypes.oneOfType([PropTypes.string, PropTypes.func]),
  listItemProps: PropTypes.shape()
};

NumberedListGroupItem.defaultProps = {
  as: "div",
  className: undefined,
  href: undefined
};

export default NumberedListGroupItem;
