# coding=UTF-8
"""
Form pour refuser une invitation.
(!) Lors de la construction on lui passe un id qui est caché :
    c'est l'id de la personne dont on refuse l'invitation
"""

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from app.forms.generic.form_hidden_field import HiddenFieldForm
from app.models.personne_enums import PersonneEnums


class PersonneInvitationRefuseForm(HiddenFieldForm):
    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Reason:')
    raison_refus = forms.IntegerField(
        label=a,
        widget=forms.Select(attrs={
            'title': a,
            'groupno': 1,
            'class': 'form-control'},
            choices=[(k, PersonneEnums.TAB_INVITATION[k])
                     for k in PersonneEnums.TAB_INVITATION],),
        error_messages=e)
