# Specification

Implement in your favorate languages by following this specification.

## Interface

Namespace should always be **GB2260**.

## Data Structure

There is a standard structure named `Division`. Those following properties
should be included in it.

- `code`: The six-digit number of the specific administrative division.
- `name`: The Chinese name of the specific administrative division.
- `year`: Optional. The revision year, and empty means "latest".

For example, a county of Beijing in JavaScript is defined like this:

```javascript
{
  "code": "110103",
  "name": "崇文区",
  "year": 2003
}
```

The administrative level representation depends on recursion records. The
division codes `XX0000` (`XX` is non-zero digits) mean provinces. And there are
`XXXX00` for prefectures and `XXXXXX` for counties.

```javascript
{
  "code": "110100",
  "name": "市辖区",
  "year": null
}
```

```javascript
{
  "code": "110000",
  "name": "北京市",
  "year": null
}
```

## Methods

Methods the interface **GB2260** MUST contains.

### `GB2260(year).get(code)`

Return the division of the given code. If `year` is not specified, use the latest data.

```javascript
GB2260().get(110103)

// =>
{
  "code": "110103",
  "name": "崇文区",
  "year": null
}
```


### `GB2260(year).provinces()` 省

Return a list of provinces in `Division` data structure.


### `GB2260(year).prefectures(province_code)` 地级市

Return a list of prefecture level cities in `Division` data structure.

A `province_code` is a 6-length province code. It can also be:

* 2-length code
* 4-length code that endswith `00`


### `GB2260(year).counties(prefecture_code)` 县

Return a list of counties in `Division` data structure.

A `prefecture_code` is a 6-length code that endswith `00`. It can also be a 4-length code.
