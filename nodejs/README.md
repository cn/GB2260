# GB/T 2260

The latest GB/T 2260 codes. Updated at 2013, published at 2014.

## Installation

Install with npm:

    $ npm install gb2260 --save

## Usage

```js
var gb2260 = require('gb2260');
```

### .data

Get data of GB/T 2260-2013.

```js
console.log(gb2260.data)
```

### .parse(code)

Parse a code, and get the city name of that code.

```js
gb2260.parse(420822)
// => '湖北省 荆门市 沙洋县'
```

## License

WTFPL
