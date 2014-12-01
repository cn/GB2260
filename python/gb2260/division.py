from __future__ import unicode_literals

import weakref

from .data import data
from ._compat import unicode_compatible, unicode_type


@unicode_compatible
class Division(object):
    """The administrative divison."""

    _identity_map = weakref.WeakValueDictionary()

    def __init__(self, code, name):
        self.code = unicode_type(code)
        self.name = unicode_type(name)

    def __repr__(self):
        return 'gb2260.Division(%r, %r)' % (self.code, self.name)

    def __str__(self):
        humanize_name = '/'.join(x.name for x in self.stack())
        return '<gb2260.Division %s %s>' % (self.code, humanize_name)

    def __hash__(self):
        return hash((self.__class__, self.code))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    @classmethod
    def get(cls, code):
        key = int(code)
        if key in cls._identity_map:
            return cls._identity_map[key]
        if key in data:
            instance = cls(code, data[key])
            cls._identity_map[key] = instance
            return instance
        raise ValueError('%r is not valid division code' % code)

    @property
    def province(self):
        return self.get(self.code[:2] + '0000')

    @property
    def is_province(self):
        return self.province == self

    @property
    def prefecture(self):
        if self.is_province:
            return
        return self.get(self.code[:4] + '00')

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
