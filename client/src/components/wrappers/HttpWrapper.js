import React from 'react';
import PropTypes from 'prop-types';

import { http, promiseUtil } from '../../util';

const baseAPIUrl = 'http://private-d88934-waterbeacon.apiary-mock.com/v1';
const endpoint = '/data';
const headers = {
  Authorization: 'JWT 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
  'Content-Type': 'application/json'
}

/**
 * HTTPWrapper
 * -----------------
 * In the future, we'll expand this to encompass different HTTP methods
 * and more flexibility for handling of success, error responses.
 * 
 * For now, this is just a stub wrappeer with hard-coded values
 * for testing API integration with the app. 
 */
class HttpWrapper extends React.Component {
  constructor() {
    super();

    this.state = {
      data: {},
      isLoading: false
    };
  }

  componentDidMount() {
    this.doFetch();
  }

  doFetch = async () => {
      this.setState({ isLoading: true }, async () => {
        try {
          const data = await http.GET({ baseURL: baseAPIUrl, url: endpoint, headers });
          return promiseUtil.promisify.call(this, this.setState)({ data, isLoading: false });
        } catch (err) {
          /**
           * TODO: Handle Error
           */
          return promiseUtil.promisify.call(this, this.setState)({ isLoading: false });
        }
      });
  }

  render() {
    const { data, isLoading } = this.state;
    return this.props.render({ data, isLoading });
  }
}

HttpWrapper.propTypes = {
  render: PropTypes.func,
  data: PropTypes.shape({})
};

HttpWrapper.defaultProps = {
  render: () => {},
  data: {}
};

export default HttpWrapper;