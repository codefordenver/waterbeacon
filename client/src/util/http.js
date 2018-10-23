import axios from 'axios';

const httpMethods = {
  GET: 'GET',
  DELETE: 'DELETE',
  HEAD: 'HEAD',
  OPTIONS: 'OPTIONS',
  POST: 'POST',
  PUT: 'PUT',
  PATCH: 'PATCH'
}

/**
 * CONFIG OBJECT FOR REQUEST
 * https://github.com/axios/axios#request-config
 */
const defConfig = {
  // url: '',
  method: httpMethods.GET,
  // baseUrl: '',
  // transformRequest: [(data, headers) => {}],
  // transformResponse: [(data) => {}],
  headers: { 'Content-Type': 'application/json' },
  // params: {},
  // paramsSerializer: (params) => {},
  data: {},
  timeout: 2500,
  // withCredentials: false,
  // adapter: (config) => {},
  // auth: {},
  responseType: 'json',
  responseEncoding: 'utf8',
  // xsrfCookieName: 'XSRF-TOKEN',
  // xsrfHeaderName: 'X-XSRF-TOKEN',
  // onUploadProgress: (progressEvent) => {},
  // onDownloadProgress: () => {},
  // maxContentLength: 2000,
  // validateStatus: (status) => {},
  // maxRedirects: 5,
  // socketPath: null,
  // httpAgent: new http.Agent({ keepAlive: true }),
  // httpsAgent: new https.Agent({ keepAlive: true }),
  // proxy: {
  //   host: '127.0.0.1',
  //   port: 9000,
  //   auth: {
  //     username: '',
  //     password: ''
  //   }
  // },
  // cancelToken: new CancelToken(function (cancel) {})
};

function request(config = {}) {
  return axios(Object.assign(defConfig, config));
}

function makeRequest(method) {
  return config => request(Object.assign(config, { method }));
};

export default Object.keys(httpMethods).reduce((expObj, method) => {
  expObj[method] = makeRequest(method);
  return expObj
}, {});
