from __future__ import unicode_literals

import weakref

from .data import data
from ._compat import unicode_compatible, unicode_type


@unicode_compatible
class Division(object):
    """The administrative divison."""

    _identity_map = dict(
        (year, weakref.WeakValueDictionary()) for year in data)

    def __init__(self, code, name, year=None):
        self.code = unicode_type(code)
        self.name = unicode_type(name)
        self.year = year

    def __repr__(self):
        if self.year is None:
            return 'gb2260.get(%r)' % self.code
        else:
            return 'gb2260.get(%r, %r)' % (self.code, self.year)

    def __str__(self):
        name = 'GB2260' if self.year is None else 'GB2260-%d' % self.year
        humanize_name = '/'.join(x.name for x in self.stack())
        return '<%s %s %s>' % (name, self.code, humanize_name)

    def __hash__(self):
        return hash((self.__class__, self.code, self.year))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.year == other.year

    @classmethod
    def get(cls, code, year=None):
        key = int(code)
        if year and year not in data:
            raise ValueError('year must be in %r' % list(data))

        cache = cls._identity_map[year]
        store = data[year]

        if key in cache:
            return cache[key]
        if key in store:
            instance = cls(code, store[key], year)
            cache[key] = instance
            return instance

        raise ValueError('%r is not valid division code' % code)

    @property
    def province(self):
        return self.get(self.code[:2] + '0000', self.year)

    @property
    def is_province(self):
        return self.province == self

    @property
    def prefecture(self):
        if self.is_province:
            return
        return self.get(self.code[:4] + '00', self.year)

    @property
    def is_prefecture(self):
        return self.prefecture == self

    @property
    def county(self):
        if self.is_province or self.is_prefecture:
            return
        return self

    @property
    def is_county(self):
        return self.county is not None

    def stack(self):
        yield self.province
        if self.is_prefecture or self.is_county:
            yield self.prefecture
        if self.is_county:
            yield self
