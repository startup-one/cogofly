# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}
    a = _('Email:')
    email_or_username = forms.CharField(
        label=a, max_length=100,
        widget=forms.TextInput(attrs={
            'title': a, 'size': 100, 'type': 'text',
            'placeholder': _('mymail@exemple.org or username'),
            'class': 'form-control'}),
        error_messages=e)

    a = _('Password:')
    password = forms.CharField(
        label=a, max_length=100,
        widget=forms.PasswordInput(attrs={
            'title': a, 'size': 30,
            'placeholder': '**************',
            'class': 'form-control'}
        ),
        error_messages=e)


class RegisterForm(forms.Form):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    # alphanumeric = RegexValidator(
    #     r'^[0-9a-zA-Z-\.]*$', _(u'Only alphanumeric characters '
    #                             u'(a..z and 0..9) are allowed'))
    # a = _(u'User name:')
    # username = forms.CharField(
    #     label=a, max_length=100,
    #     widget=forms.TextInput(attrs={'title': a,
    #                                   'placeholder': _(u'my user name')}),
    #     validators=[alphanumeric],
    #     error_messages=e.copy().update({
    #         'invalid': _(u'This field accepts only letters and numbers')
    #     }))

    a = _('First name:')
    prenom = forms.CharField(
        label=a, max_length=100,
        widget=forms.TextInput(attrs={'title': a,
                                      'placeholder': _('my first name'),
                                      'class': 'form-control'}
                               ),
        error_messages=e)

    a = _('Last name:')
    nom = forms.CharField(
        label=a, max_length=100,
        widget=forms.TextInput(attrs={'title': a,
                                      'placeholder': _('my last name'),
                                      'class': 'form-control'}),
        error_messages=e)

    a = _('Email:')
    email = forms.EmailField(
        label=a, max_length=200,
        widget=forms.TextInput(attrs={'title': a, 'size': 30, 'type': 'email',
                                      'placeholder': _('mymail@exemple.org'),
                                      'class': 'form-control'}),
        error_messages=e)

    a = _('Password:')
    password1 = forms.CharField(
        label=a, max_length=100,
        widget=forms.PasswordInput(attrs={'title': a, 'size': 30,
                                          'placeholder': '**************',
                                          'class': 'form-control'}),
        error_messages=e)

    a = _('Confirm password:')
    password2 = forms.CharField(
        label=a, max_length=100,
        widget=forms.PasswordInput(attrs={'title': a, 'size': 30,
                                          'placeholder': '**************',
                                          'class': 'form-control'}),
        error_messages=e)

