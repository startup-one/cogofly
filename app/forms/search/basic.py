# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _

from app.forms.generic.fields.field_date_partial import FormFieldDatePartial
from app.forms.widgets.google_maps import GoogleMapsWidget
from app.forms.widgets.widget_date_selector import DateSelectorWidget


class SearchBasicForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Where do you want to go?')
    travel = forms.CharField(
        # (!) laisser required=False, je le gère plus loin s'il est vide :
        label=a, max_length=100, required=False,
        widget=GoogleMapsWidget(attrs={
            'captioncolor': '#f85a29',  # champ custom
            'title': a, 'size': 100, 'type': 'text',
            'placeholder': _('town/country'),
            'rowstart': True,
            'rowend': True,
            'rowspan': 6,
            'class': 'form-control'}),
        error_messages=e)

    a = _('Start:')
    date_start = FormFieldDatePartial(
        label=a, localize=True, required=False,
        help_text=_("When?"),
        widget=DateSelectorWidget(attrs={
            'helpcolor': '#f85a29',  # champ custom
            'title': a,
            'rowstart': True,
            'rowspan': 3,
            'style': "display: inline-block; width: auto",
            'class': 'form-control'}))

    a = _('End:')
    date_end = FormFieldDatePartial(
        label=a, localize=True, required=False,
        # help_text='&nbsp;',
        widget=DateSelectorWidget(attrs={
            'formgroupclass': 'search-date-end',
            'title': a,
            'rowspan': 3,
            'rowend': True,
            'style': "display: inline-block; width: auto",
            'class': 'form-control'}))
