# coding=UTF-8

import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error
import six.moves.urllib.parse

from django import template
from django.template import Node
from django.utils.translation import ugettext_lazy as _
from url_tools.helper import UrlHelper
import six

register = template.Library()


@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "'captureas' node requires a variable name."
        )
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''


@register.filter(name='replace_linebr')
def replace_linebr(value):
    """
    Replaces all values of line break from the given string
    with a line space.

    Args:
        value: string in template
    """
    value = value.replace("\n", ' ')
    while value.find('  ') >= 0:
        value = value.replace('  ', ' ')
    value = value.replace(' >', '>')
    return value.strip()


@register.filter(name='not_empty')
def not_empty(value):
    """
    Test si None *ou* chaine vide
    Args:
        value: string in template
    """
    return value is not None and (len(value) > 0)


@register.filter(name='joinby')
def joinby(arg1, arg2):
    """
    Renvoyer "a, b, c and d" pour un tableau [a, b, c, d]
    Args:
        arg1: array
        arg2: separator
    """
    if len(arg1) < 2:
        return arg1
    l = len(arg1)-1
    return _('{} and {}').format(arg2.join([str(p) for p in arg1[:l]]),
                                  str(arg1[l]))


@register.tag(name='cleanup')
def do_cleanup(parser, token):
    """
    Replaces all line break between cleanup/endcleanup with a line space.

    Args:
        parser: see official documentation
        token: see official documentation
    """
    nodelist = parser.parse(('endcleanup',))
    parser.delete_first_token()
    return CleanupNode(nodelist)


class CleanupNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        from django.utils.html import strip_spaces_between_tags
        ret = strip_spaces_between_tags(self.nodelist.render(context).strip())
        ret = ret.replace("\n", ' ')
        while ret.find('  ') >= 0:
            ret = ret.replace("  ", ' ')
        # (!) si retours à la ligne dans les templates "toto ," -> "toto,"
        ret = ret.replace(" ,", ',')
        ret = ret.replace(" .", '.')
        return ret


@register.filter(name='url_without_parameter')
def url_without_parameter(arg1, arg2):
    """
    Removes an argument from the get URL.
    Use:
        {{ request|url_without_parameter:'page' }}

    Args:
        arg1: request
        arg2: parameter to remove
    """
    if arg1.GET.getlist(arg2):
        # get all parameters :
        full_url = six.moves.urllib.parse.urllib.parse(arg1.get_full_path())
        parameters = {}
        # reconstruct query
        for key, value in six.moves.urllib.parse.parse_qsl(full_url.query):
            if parameters.get(key, None) is None:
                parameters[key] = value
        # remove parameters
        if parameters.get(arg2) is not None:
            del parameters[arg2]
        arg1.META['QUERY_STRING'] = '&'.join([
            '{}={}'.format(key, value)
            for key, value in six.iteritems(parameters)])

    return arg1.get_full_path()


@register.filter(name='url_get_separator')
def url_get_separator(arg1):
    """
    Returns '?' or '&' if there are QUERY parameters in the URL
    Use:
        {{ request|url_get_separator }}

    Args:
        arg1: request
    """
    return '&' if arg1.META.get('QUERY_STRING', '') else '?'


@register.simple_tag
def url_replace_parameter(url, **kwargs):
    """
    Changes argument from the get URL.
    (!) BUG in the official python lib (parse_qsl() is buggy)
    Use:
        {% url_replace_parameter request.get_full_path param=value as new_url %}

    Args:
        url: request
        kwargs: parameters to add/replace
    """
    u = six.moves.urllib.parse.urllib.parse(url)
    pairs = [s2 for s1 in u.query.split('&') for s2 in s1.split(';')]
    r = {}
    for name_value in pairs:
        if not name_value:
            continue
        nv = name_value.split('=', 1)
        if len(nv) == 2:
            if len(nv[1]):
                name = nv[0]
                value = nv[1]
                # (!) BUG in the official python lib (parse_qsl() is buggy)!
                if isinstance(name, six.text_type):
                    name = name.encode('ascii')
                if isinstance(value, six.text_type):
                    value = value.encode('ascii')
                name = six.moves.urllib.parse.unquote(name.replace('+', ' '))
                value = six.moves.urllib.parse.unquote(value.replace('+', ' '))
                if name in r:
                    r[name].append(value)
                else:
                    r[name] = [value]
    # Replace with new values:
    for key, val in six.iteritems(kwargs):
        if isinstance(val, list):
            r[key] = val
        else:
            r[key] = [val]
    retour = ''
    for k, tab in six.iteritems(r):
        if len(tab) == 1:
            retour += '{}={}'.format(k, tab[0])
        else:
            retour += '&'.join(['{}={}'.format(k, val) for val in tab])
        retour += '&'
    return '{}?{}'.format(u.path, retour)
