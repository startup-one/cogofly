# coding=UTF-8

import ast

from django import forms
from django.core.exceptions import ValidationError, FieldError
from django.utils.translation import ugettext_lazy as _
import six


class TagTypedChoiceField(forms.TypedChoiceField):
    """
        Permet de créer un champ qui donne la possibilité de choisir parmi des
        valeurs OU BIEN de rajouter une valeur via la propriété custom_tag
    """

    @staticmethod
    def to_array(x):
        try:
            retour = ast.literal_eval(x)
        except SyntaxError:
            raise ValidationError(_('List required'), code='required')
        if not isinstance(retour, list):
            raise ValidationError(_('List required'), code='required')
        return retour

    def __init__(self, *args, **kwargs):
        if kwargs.pop('coerce', None):
            raise FieldError(_("coerce is overriden"), code='required')
        self.custom_tag = kwargs.pop('custom_tag', lambda val: val)
        super(TagTypedChoiceField, self).__init__(coerce=self.to_array,
                                                  *args, **kwargs)
        if not isinstance(self.empty_values, list):
            raise FieldError(_('Empty: list required'), code='required')

    def clean(self, value):
        if value is None:
            return super(TagTypedChoiceField, self).clean(value)
        elif not isinstance(value, list):
            raise ValidationError(_('List required'), code='required')
        new_values = []
        for v in value:
            if isinstance(v, six.integer_types):
                # une exception sera levée s'il n'est pas parmi les choix :
                n = super(TagTypedChoiceField, self).clean(int(v))
                new_values.append(n)
            else:
                try:
                    new_values.append(int(v))
                except ValueError:
                    try:
                        # C'est une chaîne qui n'est pas un entier -> appeler
                        # la méthode qui doit la traiter et forcer en entier :
                        pk = int(self.custom_tag(v))
                        new_values.append(pk)
                        # ajouter aux possibilités "acceptables" pour le champ :
                        self.choices.append((pk, v))
                    except ValueError:
                        raise FieldError(_("custom_tag: result should be int"),
                                         code='required')

        return super(TagTypedChoiceField, self).clean(new_values)

    def validate(self, value):
        # Dans le source, value est convertie en chaîne par to_python().
        # Ici, comme c'est une liste de choix elle ressemble à u'[1, 12, 87...]'
        # -> forcer la conversion
        try:
            if value == '':
                value = []
            else:  # ! ast.literal_eval() est un safe "eval" :
                value = ast.literal_eval(value)
        except SyntaxError:
            raise ValidationError(_('List required'), code='required')

        # Vérification que c'est bien une liste reçue :
        if not isinstance(value, list):
            raise ValidationError(_('List required'), code='required')

        # Vérification qu'il n'y a que des entiers dans la liste :
        if not all(isinstance(item, int) for item in value):
            raise ValidationError(_('List of int required'), code='required')

        # S'assurer qu'entre l'appel clean() puis validate(),
        # tout est toujours valide :
        for v in value:
            super(TagTypedChoiceField, self).validate(v)
