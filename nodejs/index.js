/**
 * GB2260 parser
 */

var data = require('./GB2260');

exports.data = data;

exports.parse = function(code) {
  code = code.toString();
  code = code.replace(/0+$/, '');
  if (code.length < 2 || code.length > 6 || code.length % 2 !== 0) {
    throw new Error('Invalid Code');
  }

  var province = data[code.slice(0, 2) + '0000'];
  if (!province) return null;

  if (code.length === 2) {
    return province;
  }

  var area = data[code.slice(0, 4) + '00'];
  if (!area) return null;

  if (code.length === 4) {
    return province + ' ' + area;
  }

  var name = data[code];
  if (!name) return null;

  return province + ' ' + area + ' ' + name;
};
