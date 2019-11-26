# coding=UTF-8
"""
Form pour accepter une invitation.
J'avais en tête qu'au moment de l'accepter, on fait comme lors du refus :
on ouvre un combo, mais là on dit le type de relation (ami, mari, prof, etc.)
Franck ne veut pas en entendre parler, tant pis.
(!) Lors de la construction on lui passe un id qui est caché :
    c'est l'id de la personne dont on accepte l'invitation
"""

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from app.forms.generic.form_hidden_field import HiddenFieldForm
from app.models.personne_enums import PersonneEnums


class PersonneInvitationAcceptForm(HiddenFieldForm):
    pass
