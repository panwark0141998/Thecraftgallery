const dns = require('dns');
const originalLookup = dns.lookup;
dns.lookup = function(hostname, options, callback) {
  if (hostname === 'api.netlify.com') {
    if (typeof options === 'function') {
      callback = options;
      options = {};
    }
    const ip = '3.19.156.32';
    if (options && options.all) {
      return callback(null, [{ address: ip, family: 4 }]);
    }
    return callback(null, ip, 4);
  }
  return originalLookup.call(dns, hostname, options, callback);
};
console.log('[DNS Preload] Intercepted dns.lookup for api.netlify.com');
