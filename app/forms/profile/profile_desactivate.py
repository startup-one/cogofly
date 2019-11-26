# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _

# from app.forms.widgets.bootstrap_choices import BootstrapRadioSelect


class ProfileDesactivateForm(forms.Form):
    YES_NO = (
        (True, _('Yes')),
        (False, _('No')),
    )
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('By clicking "Yes" you agree to desactivate your account:')
    # 'i_agree' seul est en conflit avec 'i_agree' de ProfileDeleteForm
    # -> le rendre unique via '_desactivate' :
    i_agree_desactivate = forms.TypedChoiceField(
        label=_('Still agree?'),
        required=False,
        coerce=lambda x: x == 'True',
        choices=YES_NO,
        widget=forms.RadioSelect)
