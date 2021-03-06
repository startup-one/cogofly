"""
A backport of UserDict.DictMixin for pre-python-2.4
"""

import six
__all__ = ['DictMixin']

try:
    from UserDict import DictMixin
except ImportError:
    class DictMixin:
        # Mixin defining all dictionary methods for classes that already have
        # a minimum dictionary interface including getitem, setitem, delitem,
        # and keys. Without knowledge of the subclass constructor, the mixin
        # does not define __init__() or copy().  In addition to the four base
        # methods, progressively more efficiency comes with defining
        # __contains__(), __iter__(), and iteritems().

        # second level definitions support higher levels
        def __iter__(self):
            for k in list(self.keys()):
                yield k
        def has_key(self, key):
            try:
                value = self[key]
            except KeyError:
                return False
            return True
        def __contains__(self, key):
            return key in self

        # third level takes advantage of second level definitions
        def iteritems(self):
            for k in self:
                yield (k, self[k])
        def iterkeys(self):
            return self.__iter__()

        # fourth level uses definitions from lower levels
        def itervalues(self):
            for _, v in six.iteritems(self):
                yield v
        def values(self):
            return [v for _, v in six.iteritems(self)]
        def items(self):
            return list(six.iteritems(self))
        def clear(self):
            for key in list(self.keys()):
                del self[key]
        def setdefault(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                self[key] = default
            return default
        def pop(self, key, *args):
            if len(args) > 1:
                raise TypeError("pop expected at most 2 arguments, got "\
                                  + repr(1 + len(args)))
            try:
                value = self[key]
            except KeyError:
                if args:
                    return args[0]
                raise
            del self[key]
            return value
        def popitem(self):
            try:
                k, v = six.iteritems(self)
            except StopIteration:
                raise KeyError('container is empty')
            del self[k]
            return (k, v)
        def update(self, other=None, **kwargs):
            # Make progressively weaker assumptions about "other"
            if other is None:
                pass
            elif hasattr(other, 'iteritems'):  # iteritems saves memory and lookups
                for k, v in six.iteritems(other):
                    self[k] = v
            elif hasattr(other, 'keys'):
                for k in list(other.keys()):
                    self[k] = other[k]
            else:
                for k, v in other:
                    self[k] = v
            if kwargs:
                self.update(kwargs)
        def get(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                return default
        def __repr__(self):
            return repr(dict(six.iteritems(self)))
        def __cmp__(self, other):
            if other is None:
                return 1
            if isinstance(other, DictMixin):
                other = dict(six.iteritems(other))
            return cmp(dict(six.iteritems(self)), other)
        def __len__(self):
            return len(list(self.keys()))
