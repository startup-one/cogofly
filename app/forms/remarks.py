# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _


class RemarksForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _("Feel free to contact us with any remarks or suggestions "
          "you may have, any problems you have encountered and any ways "
          "in which you feel the site could be improved in order to "
          "meet your expectations.")
    remarks = forms.CharField(
        label=a, max_length=20000,
        widget=forms.Textarea(attrs={
            'title': a, 'size': 25,
            'type': 'textarea', 'rows': '8',
            'class': 'form-control'}),
        error_messages=e)


