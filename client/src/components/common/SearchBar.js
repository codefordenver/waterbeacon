import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import { FormControl } from "react-bootstrap";

import IconButton from "./IconButton";

import "./SearchBar.css";

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: props.defaultValue };
  }

  handleChange = event => {
    if (event && event.target) {
      const { value } = event.target; 
      this.setState({ value });
    }
  }

  handleSearch = () => this.props.onSearch(this.state.value.trim());

  handleKeyDown = event => {
    if (event.keyCode === 13) {
      // <ENTER> key pressed
      return this.handleSearch();
    }
  }

  render() {
    const { className, onSearch } = this.props;

    return (
      <div className={classNames("search-bar", className)}>
        <FormControl type="text" placeholder="Search (State, City, County)" onChange={this.handleChange} onKeyDown={this.handleKeyDown} />
        <IconButton iconClassName="oi-magnifying-glass" onClick={onSearch} />
      </div>
    );
  }
}

SearchBar.propTypes = {
  className: PropTypes.string,
  defaultValue: PropTypes.string,
  onSearch: PropTypes.func
};

SearchBar.defaultProps = {
  className: undefined,
  defaultValue: "",
  onSearch: () => {}
};

export default SearchBar;
