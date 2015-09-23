# Specification

Implement in your favorite languages by following this specification.

* Version: 0.2
* Date: 2015-09-23
* Authors: Hsiaoming Yang, Jiangge Zhang


## Interface

Namespace should always be **GB2260**.

## Data Structure

There is a standard structure named `Division`. Those following properties
should be included in it.

- `code`: (str) The six-digit number of the specific administrative division.
- `name`: (str) The Chinese name of the specific administrative division.
- `revision`: (str) Optional. The revision year, and empty means "latest".

For example, a county of Beijing in JavaScript is defined like this:

```javascript
{
  "code": "110103",
  "name": "崇文区",
  "revision": "2003"
}
```

The administrative level representation depends on recursion records. The
division codes `XX0000` (`X` is non-zero digit) mean provinces. And there are
`XXXX00` for prefectures and `XXXXXX` for counties.

```javascript
{
  "code": "110100",
  "name": "市辖区",
  "revision": null
}
```

```javascript
{
  "code": "110000",
  "name": "北京市",
  "revision": null
}
```

### .province

Return province level division of current division.

### .prefecture

Return prefecture level division of current division. If current division is a province,
return none/null/nil.

### .description

A description of current division. e.g.

```
北京市 市辖区 崇文区
```

## Methods

The interface MUST have a constructor method to create a new instance:

```
gb2260 = new GB2260(str revision)
```

If `revision` is not specified, use the latest data.


### `.get(str code)`

Return the division of the given code.

```javascript
gb2260.get("110103")

// =>
{
  "code": "110103",
  "name": "崇文区",
  "revision": null
}
```


### `.provinces()` 省

Return a list of provinces in `Division` data structure.


### `.prefectures(str province_code)` 地级市

Return a list of prefecture level cities in `Division` data structure.

A `province_code` is a 6-length province code. It can also be:

* 2-length code
* 4-length code that endswith `00`


### `.counties(str prefecture_code)` 县

Return a list of counties in `Division` data structure.

A `prefecture_code` is a 6-length code that endswith `00`. It can also be a 4-length code.


### `#revisions`

List all revisions supported by GB2260. This is a module(class) constant.


### `#search(code, str[] revisions)`

This module(class) method is optional. `str[] revisions` paramter is optional,
if not specified, all revisions are used.

Search the given code in the givent revisions.


## Additional Information

The `code` value is always a string. In weak typed languages, the parameter for `code`,
`province_code` and `prefecture_code` can also be int.
