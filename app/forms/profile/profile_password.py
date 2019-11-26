# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _


class ProfilePasswordForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Old password:')
    old_password = forms.CharField(
        help_text=_('Change your password here:'),
        label=a, max_length=100, required=False,
        widget=forms.PasswordInput(attrs={
            'title': a, 'size': 30,
            'helpcolor': '#f85a29',  # champ custom
            'groupno': 0,
            'placeholder': '**************',
            'class': 'form-control'}
        ),
        error_messages=e)

    a = _('New password:')
    new_password1 = forms.CharField(
        label=a, max_length=100, required=False,
        widget=forms.PasswordInput(attrs={
            'title': a, 'size': 30,
            'groupno': 0,
            'placeholder': '**************',
            'class': 'form-control'}
        ),
        error_messages=e)

    a = _('Retype the new password:')
    new_password2 = forms.CharField(
        label=a, max_length=100, required=False,
        widget=forms.PasswordInput(attrs={
            'title': a, 'size': 30,
            'groupno': 0,
            'placeholder': '**************',
            'class': 'form-control'}
        ),
        error_messages=e)

    def __init__(self, show_field_old_password=True, *args, **kwargs):
        super(ProfilePasswordForm, self).__init__(*args, **kwargs)
        if not show_field_old_password:
            # on a demandé un reset de son password par mail :
            del self.fields['old_password']

    def clean(self):
        return super(ProfilePasswordForm, self).clean()

    def save(self, commit=True):
        # (!) À la main :
        return super(ProfilePasswordForm, self).save(commit)
