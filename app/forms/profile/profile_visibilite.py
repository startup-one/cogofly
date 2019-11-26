# coding=UTF-8

from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _
# from app.forms.generic.fields.checkbox_input_bootstrap import \
#     forms.CheckboxInput
from app.forms.generic.generic import SpecialTagTypedChoiceField, \
    FormForceLocalizedDateFields
from app.models.personne import Personne
from app.models.personne_enums import PersonneEnums


class ProfileVisibiliteForm(SpecialTagTypedChoiceField,
                            FormForceLocalizedDateFields):


    class Meta:
        model = Personne
        fields = ('niveau_visibilite',
                  'age_visible', 'nb_enfants_visible', 'langue_visible',
                  'langues2_visible',
                  'niveau_etudes_visible', 'programme_visible',
                  'employer_current_visible', 'employer_previous_visible',
                  'profession_visible', 'activite_visible',
                  'hobbies_visible', 'conduite_visible',
                  'personnalite_visible', 'est_fumeur_visible',
                  'custom_zodiac_sign_visible', 'self_description_visible',)

    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _("<span style=\"padding-bottom: 10px; display: inline-block;\">"
          "Who can see my profile?"
          "</span>")
    niveau_visibilite = forms.IntegerField(
        label=a,
        help_text=_("Visibility"),
        widget=forms.Select(attrs={
            'captioncolor': '#f85a29',  # champ custom
            'title': a,
            'groupno': 0,
            'class': 'form-control'},
            choices=[(k, PersonneEnums.TAB_VISIBILITE[k])
                     for k in PersonneEnums.TAB_VISIBILITE]),
        error_messages=e)

    a = _("Show your age")
    # ! forms.CheckboxInput = bootstrap -> enlever 'class': 'form-control'
    age_visible = forms.BooleanField(
        label=a, required=False,
        help_text=_("What do you want to show?"),
        widget=forms.CheckboxInput(attrs={
            'helpcolor': '#f85a29',  # champ custom
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show number of children")
    # ! forms.CheckboxInput = bootstrap -> enlever 'class': 'form-control'
    nb_enfants_visible = forms.BooleanField(
        label=a, required=False,
        widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show the language you talk")
    # ! forms.CheckboxInput = bootstrap -> enlever 'class': 'form-control'
    langue_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show other languages you talk")
    # ! forms.CheckboxInput = bootstrap -> enlever 'class': 'form-control'
    langues2_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show your level of education")
    # ! forms.CheckboxInput = bootstrap -> enlever 'class': 'form-control'
    niveau_etudes_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show your program")
    programme_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show your current employer")
    employer_current_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show your previous employer")
    employer_previous_visible = forms.BooleanField(
        label=a, required=False,
        widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show your job")
    profession_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 1, }),
        error_messages=e)

    a = _("Show your activity")
    activite_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show your hobbies")
    hobbies_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show your driving licence")
    conduite_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show your personality")
    personnalite_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show if you're a smoker")
    est_fumeur_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show your zodiacal sign")
    custom_zodiac_sign_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    a = _("Show your self-description")
    self_description_visible = forms.BooleanField(
        label=a, required=False, widget=forms.CheckboxInput(attrs={
            'title': a,
            'groupno': 2, }),
        error_messages=e)

    def __init__(self, *args, **kwargs):
        super(ProfileVisibiliteForm, self).__init__(*args, **kwargs)
        # --------------------------------------------------------------------
        # Problème : self.fields est de type OrderedDict(), qui se base sur
        #            l'ordre d'ajout des éléments. Alors si on veut un autre
        #            ordre, pas d'autre choix que de reconstruire
        #            le dictionnaire en y appliquant l'ordre qu'on veut :
        new_fields = OrderedDict([
            ('niveau_visibilite', self.fields['niveau_visibilite']),
            ('age_visible', self.fields['age_visible']),
            ('nb_enfants_visible', self.fields['nb_enfants_visible']),
            ('langue_visible', self.fields['langue_visible']),
            ('langues2_visible', self.fields['langues2_visible']),
            ('niveau_etudes_visible', self.fields['niveau_etudes_visible']),
            ('programme_visible', self.fields['programme_visible']),
            ('employer_current_visible',
             self.fields['employer_current_visible']),
            ('employer_previous_visible',
             self.fields['employer_previous_visible']),
            ('profession_visible', self.fields['profession_visible']),
            ('activite_visible', self.fields['activite_visible']),
            ('hobbies_visible', self.fields['hobbies_visible']),
            ('conduite_visible', self.fields['conduite_visible']),
            ('personnalite_visible', self.fields['personnalite_visible']),
            ('est_fumeur_visible', self.fields['est_fumeur_visible']),
            ('custom_zodiac_sign_visible',
             self.fields['custom_zodiac_sign_visible']),
            ('self_description_visible',
             self.fields['self_description_visible']),
        ])
        for k, v in list(self.fields.items()):
            if not new_fields.get(k):  # (!) que s'ils n'y sont pas
                new_fields[k] = v
        self.fields = new_fields

    def save(self, commit=True):
        retour = super(ProfileVisibiliteForm, self).save(commit)
        return retour

    def save_instance(self, form, instance, fields=None, fail_message='saved',
                      commit=True, exclude=None, construct=True):
        a = super(ProfileVisibiliteForm, self).save_instance(
            form, instance, fields, fail_message, commit, exclude, construct)
        return a
