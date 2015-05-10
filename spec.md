# Specification

Implement in your favorate languages by following this specification.

## Namespace

Namespace should always be **GB2260**.

## Data Structure

There is a standard structure named `Division`. Those following properties
should be included in it.

- `code`: The six-digit number of the specific administrative division.
- `name`: The Chinese name of the specific administrative division.
- `year`: Optional. The revision year, and empty means "latest".

For example, a county of Beijing in JavaScript is defined like this:

``` javascript
{
  "code": "110103",
  "name": "崇文区",
  "year": 2003
}
```

The administrative level representation depends on recursion records. The
division codes `XX0000` (`XX` is non-zero digits) mean provinces. And there are
`XXXX00` for prefectures and `XXXXXX` for counties.

``` javascript
{
  "code": "110100",
  "name": "市辖区",
  "year": null
}
```

``` javascript
{
  "code": "110000",
  "name": "北京市",
  "year": null
}
```

## Methods
