# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _

from app.forms.generic.fields.checkbox_input_bootstrap import \
    CheckboxInputBootstrap


class TestimonyForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Your testimonies and positive feedback are '
          'paramount in helping Cogofly go that extra mile...'
          'They will also motivate new members to join this new community '
          'of Cogoflyers! '
          '<br/><br/>'
          'These same testimonies will appear on '
          'your contacts\' news feed and will be available to view '
          'at any time via the link "Testimonies" below')
    testimony = forms.CharField(
        label=a, max_length=20000,
        widget=forms.Textarea(attrs={
            'title': a,
            'size': 25,
            'type': 'textarea', 'rows': '8',
            'class': 'form-control'}),
        error_messages=e)

    a = _("Check if you agree to add your name, and your photo profile, "
          "inside the testimony")
    testimony_show_name = forms.BooleanField(
        label=a, required=True,
        widget=forms.CheckboxInput(attrs={
            'title': a, }),
        error_messages=e)

