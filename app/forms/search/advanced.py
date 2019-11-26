# coding=UTF-8

from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from app.forms.generic import FormFieldDatePartial, TagTypedChoiceField
# from app.forms.generic.fields.select_multiple_bootstrap import \
#     forms.CheckboxSelectMultiple
from app.forms.generic.generic import SpecialTagTypedChoiceField
from app.forms.widgets.google_maps import GoogleMapsWidget
from app.forms.widgets.widget_date_selector import DateSelectorWidget
from app.models.personne_enums import PersonneEnums
from app.models.tag import BaseTag, TagBase


class SearchAdvancedForm(SpecialTagTypedChoiceField, forms.Form):

    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Where do you want to go?')
    travel = forms.CharField(
        # (!) laisser required=False, je le gère plus loin s'il est vide :
        label=a, max_length=100, required=False,
        widget=GoogleMapsWidget(attrs={
            'captioncolor': '#f85a29',  # champ custom
            'title': a, 'size': 100, 'type': 'text',
            'placeholder': _('town/country'),
            'class': 'form-control',
            'rowstart': True,
            'rowend': True,
            'rowspan': 6,
        }),
        error_messages=e)

    a = _('Start:')
    date_start = FormFieldDatePartial(
        label=a, localize=True, required=False,
        help_text=_("When?"),
        widget=DateSelectorWidget(attrs={
            'helpcolor': '#f85a29',  # champ custom
            'title': a,
            'style': "display: inline-block; width: auto",
            'rowstart': True,
            'class': 'form-control',
            'rowspan': 3,
        }))

    a = _('End:')
    date_end = FormFieldDatePartial(
        label=a, localize=True, required=False,
        #   help_text='&nbsp;',
        widget=DateSelectorWidget(attrs={
            'formgroupclass': 'search-date-end',
            'title': a,
            'style': "display: inline-block; width: auto",
            'class': 'form-control',
            'rowspan': 3,
            'rowend': True,
        }))

    a = _('Sex:')
    sexe = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(
            attrs={'title': a,
                   'class': 'form-control',
                   'spaceabove': True,  # champ custom
                   'rowspan': 2,
                   'rowstart': True, },
            choices=[('', '--')] + [(k, PersonneEnums.TAB_SEXE[k])
                                    for k in PersonneEnums.TAB_SEXE]),
        error_messages=e)

    # a = _(u'Statut:')
    # statut = forms.IntegerField(
    #     label=a, required=False,
    #     widget=forms.Select(
    #         attrs={'title': a,
    #                'class': 'form-control',
    #                'rowspan': 2, },
    #         choices=[('', '--')] + [(k, PersonneEnums.TAB_STATUT[k])
    #                                 for k in PersonneEnums.TAB_STATUT]),
    #     error_messages=e)

    a = _('Children:')
    nb_enfants = forms.IntegerField(
        label=a, required=False,
        widget=forms.NumberInput(attrs={
            'title': a,
            'min': 0,
            'max': 15,
            'class': 'form-control',
            'rowspan': 2,
            'rowend': True, }),
        error_messages=e)

    a = _('Mother tongue:')
    langue = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(
            attrs={'title': a,
                   'class': 'form-control',
                   'rowspan': 2,
                   'rowstart': True, },
            choices=[('', '--')] + [(k, PersonneEnums.TAB_LANGUE[k])
                                    for k in PersonneEnums.TAB_LANGUE]),
        error_messages=e)

    a = _('Level of education:')
    niveau_etudes = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(
            attrs={'title': a,
                   'class': 'form-control',
                   'rowspan': 2, },
            choices=[('', '--')] + [(k, PersonneEnums.TAB_NIVEAU_ETUDES[k])
                                    for k in PersonneEnums.TAB_NIVEAU_ETUDES]),
        error_messages=e)

    a = _('Job:')
    profession = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(
            attrs={'title': a,
                   'class': 'form-control',
                   'rowspan': 2, },
            choices=[('', '--')] + [(k, PersonneEnums.TAB_PROFESSION[k])
                                    for k in PersonneEnums.TAB_PROFESSION]),
        error_messages=e)

    a = _('Smoker:')
    est_fumeur = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(
            attrs={'title': a,
                   'class': 'form-control',
                   'rowstart': True,
                   'rowspan': 2, },
            choices=[('', '--')] + [(k, PersonneEnums.TAB_EST_FUMEUR[k])
                                    for k in PersonneEnums.TAB_EST_FUMEUR]),
        error_messages=e)

    a = _('Star sign:')
    custom_zodiac_sign = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(
            attrs={'title': a,
                   'class': 'form-control',
                   'rowspan': 2,
                   'rowend': True, },
            choices=[('', '--')] +
                    [(k, PersonneEnums.TAB_CUSTOM_ZODIAC_SIGN[k])
                     for k in PersonneEnums.TAB_CUSTOM_ZODIAC_SIGN]),
        error_messages=e)

    def __init__(self, *args, **kwargs):
        super(SearchAdvancedForm, self).__init__(*args, **kwargs)

        a = _('Current employer:')
        field_employer_current = forms.CharField(
            label=a, max_length=100, required=False,
            widget=GoogleMapsWidget(
                attrs={'title': a, 'size': 100, 'type': 'text',
                       'placeholder': _('current employer'),
                       'class': 'form-control',
                       'rowstart': True,
                       'rowspan': 2, }),
            error_messages=self.e)

        a = _('Previous employer:')
        field_employer_previous = forms.CharField(
            label=a, max_length=100, required=False,
            widget=GoogleMapsWidget(
                attrs={'title': a, 'size': 100, 'type': 'text',
                       'placeholder': _('previous employer'),
                       'class': 'form-control',
                       'rowspan': 2, }),
            error_messages=self.e)

        """
        (!!) 10 jours de boulot perdus !!
        # --------------------------------------------------------------------
        # Known languages :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_languages(value):
            return self.add_tag_to(value, BaseTag.TYPE_LANGUE)

        a = _(u'Known languages:')
        known_languages = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_languages,
            widget=Select2Widget(attrs={
                'title': a,
                'rowstart': True,
                'rowspan': 3,
                'placeholder': _(u'type here your known languages'),
                'multiple': 'multiple',
                'data-select2-json': reverse_lazy('json_tag_langages'),
                'class': 'form-control'}),
            error_messages=self.e,
            choices=self.get_list_tags(BaseTag.TYPE_LANGUE))

        # --------------------------------------------------------------------
        # Types de permis :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_type_permis(value):
            return self.add_tag_to(value, BaseTag.TYPE_PERMIS)

        a = _(u'Driving licences:')
        types_permis = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_type_permis,
            widget=Select2Widget(attrs={
                'title': a,
                'rowspan': 3,
                'placeholder': _(u'type here all your driving licences'),
                'multiple': 'multiple',
                'data-select2-json': reverse_lazy('json_tag_types_permis'),
                'class': 'form-control'}),
            error_messages=self.e,
            choices=self.get_list_tags(BaseTag.TYPE_PERMIS))

        # --------------------------------------------------------------------
        # Diplômes :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_diplomas(value):
            return self.add_tag_to(value, BaseTag.TYPE_DIPLOME)

        a = _(u'Diplomas:')
        diplomes = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_diplomas,
            widget=Select2Widget(attrs={
                'title': a,
                'rowspan': 3,
                'placeholder': _(u'type here all your diplomas'),
                'multiple': 'multiple',
                'data-select2-json': reverse_lazy('json_tag_diplomes'),
                'class': 'form-control'}),
            error_messages=self.e,
            choices=self.get_list_tags(BaseTag.TYPE_DIPLOME))

        # --------------------------------------------------------------------
        # Centres d'intérêt :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_centres_dinteret(value):
            return self.add_tag_to(value, BaseTag.TYPE_CENTRE_DINTERET)

        a = _(u'Points of interest:')
        centres_dinteret = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_centres_dinteret,
            widget=Select2Widget(attrs={
                'title': a,
                'rowspan': 3,
                'rowend': True,
                'placeholder': _(u'type here all your points of interest'),
                'multiple': 'multiple',
                'data-select2-json': reverse_lazy('json_tag_centres_dinteret'),
                'class': 'form-control'}),
            error_messages=self.e,
            choices=self.get_list_tags(BaseTag.TYPE_CENTRE_DINTERET))

        """

        # --------------------------------------------------------------------
        # Programmes :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_programmes(value):
            return self.add_tag_to(value, TagBase.TYPE_MATIERE)

        a = _('Subjects')
        programmes2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_programmes,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title': a,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 2,
                'rowend': True, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_MATIERE))

        # --------------------------------------------------------------------
        # Activities :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_activities(value):
            return self.add_tag_to(value, TagBase.TYPE_ACTIVITE)

        a = _('Activity sectors:')
        activites2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_activities,
            
            widget=forms.CheckboxSelectMultiple(attrs={
                'title': a,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 3,
                'rowend': True, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_ACTIVITE))

        # --------------------------------------------------------------------
        # Hobbies :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de ses hobbies.
        def add_tag_to_hobbies(value):
            return self.add_tag_to(value, TagBase.TYPE_HOBBY)
        a = _('Hobbies')
        hobbies2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_hobbies,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title': a,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowstart': True,
                'rowspan': 2, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_HOBBY))

        # --------------------------------------------------------------------
        # Types de permis :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_types_permis(value):
            return self.add_tag_to(value, TagBase.TYPE_PERMIS)
        a = _('Licences')
        types_permis2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_types_permis,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title': a,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 2,
                'rowend': True, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_PERMIS))

        # --------------------------------------------------------------------
        # Personnalités :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_personnalites(value):
            return self.add_tag_to(value, TagBase.TYPE_PERSONNALITE)
        a = _('Personalities')
        personnalites2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_personnalites,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title': a,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 2, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_PERSONNALITE))

        # --------------------------------------------------------------------
        # Langues :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_langues(value):
            return self.add_tag_to(value, TagBase.TYPE_LANGUE)
        a = _('Spoken languages')
        langues2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_langues,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title': a,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 2, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_LANGUE))

        a = _('Age:')
        age = forms.IntegerField(
            label=a, required=False,
            widget=forms.Select(
                attrs={'title': a,
                       'class': 'form-control',
                       'rowspan': 2, },
                choices=[('', '--')] + [(k, PersonneEnums.TAB_AGE[k])
                                        for k in PersonneEnums.TAB_AGE]),
            error_messages=self.e)

        # --------------------------------------------------------------------
        # Problème : self.fields est de type OrderedDict(), qui se base sur
        #            l'ordre d'ajout des éléments. Alors si on veut un autre
        #            ordre, pas d'autre choix que de reconstruire
        #            le dictionnaire en y appliquant l'ordre qu'on veut :
        new_fields = OrderedDict([
            ('travel', self.fields['travel']),
            ('date_start', self.fields['date_start']),
            ('date_end', self.fields['date_end']),
            ('sexe', self.fields['sexe']),
            # tant que pas de premium, pas de statut :
            # ('statut', self.fields['statut']),
            ('age', age),
            ('nb_enfants', self.fields['nb_enfants']),
            ('langue', self.fields['langue']),
            ('langues2', langues2),
            ('niveau_etudes', self.fields['niveau_etudes']),
            ('programmes2', programmes2),
            ('field_employer_current', field_employer_current),
            ('field_employer_previous', field_employer_previous),
            ('profession', self.fields['profession']),
            ('activites2', activites2),
            ('hobbies2', hobbies2),
            ('personnalites2', personnalites2),
            ('types_permis2', types_permis2),
            ('est_fumeur', self.fields['est_fumeur']),
            ('custom_zodiac_sign', self.fields['custom_zodiac_sign']),
        ])
        for k, v in list(self.fields.items()):
            if not new_fields.get(k):  # (!) que s'ils n'y sont pas
                new_fields[k] = v

        self.fields = new_fields
