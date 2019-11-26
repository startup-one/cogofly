# coding=UTF-8
"""
Forme à laquelle je passe un champ avec une valeur cachée, par exemple,
au moment où j'écris :
 - pour accepter une invitation, je construis le combo et l'id = id personne dst
 - pour refuser une invitation, je construis le combo et l'id = id personne dst
 - pour envoyer un message, l'id = soit id activité, soit id conversation
 - etc.
"""

from django import forms


class HiddenFieldForm(forms.Form):

    def __init__(self, obj_bd, champ, *args, **kwargs):
        super(HiddenFieldForm, self).__init__(*args, **kwargs)

        # ! No label for hidden fields:
        id_obj = forms.IntegerField(label='',
                                    widget=forms.HiddenInput(attrs={
                                        'value': obj_bd.pk
                                    }))
        # Add field so it's in the final form
        self.fields.update({champ: id_obj})
