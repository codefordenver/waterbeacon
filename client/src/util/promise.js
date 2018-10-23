function promisify(func) {
  var that = this;
  if (typeof func !== 'function') {
    throw new TypeError('Expected an argument of type "function", but got ' + typeof func);
  }
  return function(/* ...args */) {
    var args = Array.prototype.slice.call(arguments);
    return new Promise(function(resolve, reject) {
      func.apply(that, args.concat(function(err, result) {
        if (err) reject(err);
        resolve(result);
      }));
    });
  }
}

export default { promisify };