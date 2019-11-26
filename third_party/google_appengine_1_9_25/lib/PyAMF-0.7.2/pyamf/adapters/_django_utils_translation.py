# Copyright (c) The PyAMF Project.
# See LICENSE.txt for details.

"""
C{django.utils.translation} adapter module.

@see: U{Django Project<http://www.djangoproject.com>}
@since: 0.4.2
"""


from django.utils.translation import ugettext_lazy

import pyamf
import six


def convert_lazy(l, encoder=None):
    try:
        if l.__class__._delegate_text:
            return six.text_type(l)
    except AttributeError:
        if l.__class__._delegate_unicode:
            return six.text_type(l)

    if l.__class__._delegate_str:
        return str(l)

    raise ValueError('Don\'t know how to convert lazy value %s' % (repr(l),))


pyamf.add_type(type(ugettext_lazy('foo')), convert_lazy)
