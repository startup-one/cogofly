# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _


class InviteFriendForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}
    a = _('First name:')
    prenom = forms.CharField(
        label=a, max_length=100, required=False,
        widget=forms.TextInput(attrs={'title': a,
                                      'placeholder': _('his/her first name'),
                                      'class': 'form-control'}
                               ),
        error_messages=e)

    a = _('Last name:')
    nom = forms.CharField(
        label=a, max_length=100, required=False,
        widget=forms.TextInput(attrs={'title': a,
                                      'placeholder': _('his/her last name'),
                                      'class': 'form-control'}),
        error_messages=e)

    a = _('Email:')
    email = forms.EmailField(
        label=a, max_length=200,
        widget=forms.TextInput(attrs={'title': a, 'size': 30, 'type': 'email',
                                      'placeholder': _('mail@exemple.org'),
                                      'class': 'form-control'}),
        error_messages=e)

    a = _('Personal message (optional):')
    message = forms.CharField(
        label=a, max_length=1000,
        widget=forms.Textarea(attrs={
            'title': a, 'size': 30,
            'type': 'textarea', 'rows': '9',
            'class': 'form-control'}),
        error_messages=e)


