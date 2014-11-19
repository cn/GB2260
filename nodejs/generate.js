/**
 * Generate data file for NodeJS.
 */

var fs = require('fs');
var text = fs.readFileSync(__dirname + '/../GB2260.txt', 'utf8');

var lines = text.trim().split('\n');
var rv = {};

lines.forEach(function(line) {
  var bits = line.split('\t');
  rv[bits[0]] = bits[1];
});

console.log(JSON.stringify(rv, null, 2));
