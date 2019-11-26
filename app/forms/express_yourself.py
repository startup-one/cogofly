# coding=UTF-8
"""
Form to express yourself on the wall.
"""


from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class ExpressYourselfForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    # !! No label here, exceptional:
    a = _('Express yourself:')
    express_yourself = forms.CharField(
        label='', localize=True, required=False,
        widget=widgets.Textarea(attrs={
            'groupno': 0,
            'title': a,
            'rows': 5,
            'cols': 40,
            'style': 'resize: vertical',
            'placeholder':
                _("Express yourself:\n\nYou've been away together!\n"
                  "Talk about your encounter, "
                  "your destination and your adventure in general.\n"
                  "Inspire your other contacts..."),
            'class': 'form-control'}))

