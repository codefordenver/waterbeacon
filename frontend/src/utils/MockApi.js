import axios from "axios";

// export default axios.create({
//   baseURL: "https://private-19c08-waterbeacon.apiary-mock.com/v1",
//   responseType: "json"
// });

export default axios.get('https://private-19c08-waterbeacon.apiary-mock.com/v1/data’)
.then(function (response) {
  console.log("SUCCESS": + response)
console.log(response);
})
.catch(function (error) {
  console.log("ERROR": + response)
console.log(error);
})
.then(function () {
// always executed
});
