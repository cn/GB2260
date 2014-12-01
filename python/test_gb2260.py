# coding: utf-8

from __future__ import unicode_literals

from pytest import mark

from gb2260 import Division, get


@mark.parametrize('code,stack_name,is_province,is_prefecture,is_county', [
    ('110101', u'北京市/市辖区/东城区', False, False, True),
    ('110100', u'北京市/市辖区', False, True, False),
    ('110000', u'北京市', True, False, False),
])
def test_division(code, stack_name, is_province, is_prefecture, is_county):
    division = get(code)
    assert division.code == code
    assert division.is_province == is_province
    assert division.is_prefecture == is_prefecture
    assert division.is_county == is_county
    assert '/'.join(x.name for x in division.stack()) == stack_name


def test_comparable():
    assert get(110101) == Division(110101, u'东城区')
    assert get(110101) != Division(110000, u'北京市')


def test_hashable():
    division_set = set([
        Division(110101, u'东城区'),
        Division(110000, u'北京市'),
        Division(110101, u'东城区'),
    ])
    assert division_set == set([
        Division(110101, u'东城区'),
        Division(110000, u'北京市'),
    ])
