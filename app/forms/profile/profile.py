# coding=UTF-8


import datetime
from collections import OrderedDict

from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.utils import ErrorList
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from app.forms.generic import TagTypedChoiceField
# from app.forms.generic.fields.select_multiple_bootstrap import \
#     forms.CheckboxSelectMultiple
from app.forms.generic.generic import SpecialTagTypedChoiceField, \
    FormForceLocalizedDateFields, UploadedPictureHandler
from app.forms.widgets.google_maps import GoogleMapsWidget
from app.forms.widgets.widget_date_selector import DateSelectorWidget
from app.models.generic import Langue
from app.models.tag import Tag, BaseTag, TagBase
from app.models.personne import Photo, Personne
from app.models.personne_enums import PersonneEnums
from six.moves import range


class ProfileForm(SpecialTagTypedChoiceField, FormForceLocalizedDateFields):

    class Meta:
        model = Personne
        fields = ('sexe', 'nb_enfants',
                  # cacher tant que pas de premium
                  # 'statut',
                  'est_fumeur',
                  'date_naissance', 'self_description',
                  'niveau_etudes', 'profession',
                  'programmes2', 'activites2', 'hobbies2', 'types_permis2',
                  'personnalites2', 'langues2',
                  'langue', 'how_did_i_know_cogofly',
                  'place_i_live', 'place_of_birth',
                  'employer_current', 'employer_previous',
                  'custom_zodiac_sign')

    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Email:')
    email = forms.CharField(
        label=a, max_length=100,
        widget=forms.TextInput(attrs={
            'title':'test', 'size': 100, 'type': 'text',
            'placeholder': _('mymail@exemple.org or username'),
            'groupno': 2,
            'class': 'form-control'}),
        error_messages=e)

    a = '{}<span class="important-field">*</span>'.format(_('Sex:'))
    sexe = forms.IntegerField(
        label=a,
        widget=forms.Select(attrs={
            #  'title':'test', <- pas échappé -> pas mettre
            'groupno': 2,
            'class': 'form-control'},
            choices=[('', '--')] + [(k, PersonneEnums.TAB_SEXE[k])
                                    for k in PersonneEnums.TAB_SEXE]),
        error_messages=e)

    a = _('Children:')
    nb_enfants = forms.IntegerField(
        label=a,
        widget=forms.Select(attrs={
            'title':'test',
            'groupno': 3,
            'rowstart': True,
            'rowspan': 6,
            'class': 'form-control'},
            choices=[('', '--')] + [(str(k), str(k)) for k in range(0, 15)]),
        # widget=forms.NumberInput(attrs={
        #     'min': 0,
        #     'max': 15,
        #     'title':'test',
        #     'groupno': 3,
        #     'rowstart': True,
        #     'rowspan': 6,
        #     'class': 'form-control'}),
        error_messages=e)

    # a = _(u'Statut:')
    # statut = forms.IntegerField(
    #     label=a,
    #     widget=forms.Select(attrs={
    #         'title':'test',
    #         'groupno': 2,
    #         'class': 'form-control'},
    #         choices=[('', '--')] + [(k, PersonneEnums.TAB_STATUT[k])
    #                                 for k in PersonneEnums.TAB_STATUT],),
    #     required=False,
    #     error_messages=e)

    a = _('Smoker:')
    est_fumeur = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(attrs={
            'title':'test',
            'groupno': 3,
            'rowend': True,
            'rowspan': 6,
            'class': 'form-control'},
            choices=[('', '--')] + [(k, PersonneEnums.TAB_EST_FUMEUR[k])
                                    for k in PersonneEnums.TAB_EST_FUMEUR]),
        error_messages=e)

    a = _('Date of birth: <span class="important-field">*</span>')
    date_naissance = forms.DateField(
        label=a, localize=True, required=True,
        widget=DateSelectorWidget(attrs={
            'min': 1930,
            'max': now().replace(year=now().year-18).year,  # 18 ans min.
            #  'title':'test', <- pas échappé -> pas mettre
            'style': "display: inline-block; width: auto",
            'groupno': 2,
            'class': 'form-control'}))  # -> suppression classe 'datetimepicker'

    a = _('Describe yourself:')
    self_description = forms.CharField(
        label=a, localize=True, required=False,
        widget=widgets.Textarea(attrs={
            'title':'test',
            'rows': 3,
            'groupno': 3,
            'class': 'form-control'}))

    a = _('Level of education:')
    niveau_etudes = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(attrs={
            'title':'test',
            'groupno': 3,
            'rowspan': 6,
            'rowstart': True,
            'class': 'form-control'},
            choices=[('', '--')] + [(k, PersonneEnums.TAB_NIVEAU_ETUDES[k])
                                    for k in PersonneEnums.TAB_NIVEAU_ETUDES]),
        error_messages=e)

    a = _('Job:')
    profession = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(attrs={
            'title':'test',
            'groupno': 3,
            'rowstart': True,
            'rowspan': 6,
            'class': 'form-control'},
            choices=[('', '--')] + [(k, PersonneEnums.TAB_PROFESSION[k])
                                    for k in PersonneEnums.TAB_PROFESSION]),
        error_messages=e)

    a = _('Mother tongue: <span class="important-field">*</span>')
    langue = forms.IntegerField(
        label=a, required=True,
        widget=forms.Select(attrs={
            #  'title':'test', <- pas échappé -> pas mettre
            'groupno': 2,
            'class': 'form-control', },
            choices=[('', '--')] + [(k, PersonneEnums.TAB_LANGUE[k])
                                    for k in PersonneEnums.TAB_LANGUE]),
        error_messages=e)

    a = _('How did you know Cogofly? '
          '<span style="font-size: smaller">'
          'Important: a Cogoflyer may be close...'
          '</span>')
    how_did_i_know_cogofly = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(attrs={
            #  'title':'test', <- pas échappé -> pas mettre
            'groupno': 2,
            'class': 'form-control', },
            choices=[('', '--')] +
                    [(k, PersonneEnums.TAB_HOW_DID_I_KNOW_COGOFLY[k])
                     for k in PersonneEnums.TAB_HOW_DID_I_KNOW_COGOFLY]),
        error_messages=e)

    a = _('Star sign:')
    custom_zodiac_sign = forms.IntegerField(
        label=a, required=False,
        widget=forms.Select(attrs={
            'title':'test',
            'groupno': 3,
            'rowstart': True,
            'rowspan': 6,
            'rowend': True,
            'class': 'form-control'},
            choices=[('', '--')] +
                    [(k, PersonneEnums.TAB_CUSTOM_ZODIAC_SIGN[k])
                     for k in PersonneEnums.TAB_CUSTOM_ZODIAC_SIGN]),
        error_messages=e)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.current_langue = None
        a = _('Picture:')
        field_picture = forms.ImageField(
            label=a, allow_empty_file=True, required=False,
            widget=forms.FileInput(attrs={
                'title':'test',
                'placeholder': _('my picture'),
                'accept': "image/*",
                'groupno': 0,
                'class': 'form-control', }),
            error_messages=self.e)

        a = _('Banner/background picture:')
        field_picture_banner = forms.ImageField(
            label=a, allow_empty_file=True, required=False,
            widget=forms.FileInput(attrs={
                'title':'test',
                'placeholder': _('my banner'),
                'groupno': 1,
                'accept': "image/*",
                'class': 'form-control', }),
            error_messages=self.e)

        a = _('First name:')
        user_first_name = forms.CharField(
            label=a, max_length=100,
            widget=forms.TextInput(attrs={
                'title':'test', 'size': 100, 'type': 'text',
                'placeholder': _('my first name'),
                'groupno': 2,
                'class': 'form-control'}),
            error_messages=self.e)

        a = _('Last name:')
        user_last_name = forms.CharField(
            label=a, max_length=100,
            widget=forms.TextInput(attrs={
                'title':'test', 'size': 100, 'type': 'text',
                'placeholder': _('my last name'),
                'groupno': 2,
                'class': 'form-control'}),
            error_messages=self.e)

        a = _('Town/Country of birth')
        field_place_of_birth = forms.CharField(
            label=a, max_length=100,
            widget=GoogleMapsWidget(attrs={
                'title':'test', 'size': 100, 'type': 'text',
                'placeholder': _('my town/country of birth'),
                'groupno': 2,
                'class': 'form-control'}),
            error_messages=self.e,
            required=False)

        a = _('Town/Country where I live:') + ' <span ' \
                                               'class="important-field">' \
                                               '*</span>'
        field_place_i_live = forms.CharField(
            label=a, max_length=100,
            widget=GoogleMapsWidget(attrs={
                #  'title':'test', <- pas échappé -> pas mettre
                'size': 100, 'type': 'text',
                'placeholder': _('town where I live'),
                'groupno': 2,
                'class': 'form-control'}),
            error_messages=self.e)

        a = _('Current employer:')
        field_employer_current = forms.CharField(
            label=a, max_length=100, required=False,
            widget=GoogleMapsWidget(attrs={
                'title':'test', 'size': 100, 'type': 'text',
                'placeholder': _('current employer'),
                'groupno': 3,
                'rowstart': True,
                'rowspan': 6,
                'class': 'form-control'}),
            error_messages=self.e)

        a = _('Previous employer:')
        field_employer_previous = forms.CharField(
            label=a, max_length=100, required=False,
            widget=GoogleMapsWidget(attrs={
                'title':'test', 'size': 100, 'type': 'text',
                'placeholder': _('previous employer'),
                'groupno': 3,
                'rowspan': 6,
                'rowend': True,
                'class': 'form-control'}),
            error_messages=self.e)
        """
        (!!) Suppression sur demande de Franck !! 15 jours de boulot perdus !!
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
                'title':'test',
                'groupno': 3,
                'multiple': 'multiple',
                'rowspan': 6,
                'rowend': True,
                'class': 'form-group'}),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_MATIERE))

        # --------------------------------------------------------------------
        # Activites :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_activites(value):
            return self.add_tag_to(value, TagBase.TYPE_ACTIVITE)

        a = _('Activity sectors:')
        activites2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_activites,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title':'test',
                'groupno': 3,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 6,
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
                'title':'test',
                'groupno': 3,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 6,
                'rowstart': True, }),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_HOBBY))

        # --------------------------------------------------------------------
        # Types de permis :
        # --> Pré-remplir avec les choix déjà faits avec tous ceux possibles
        #     de sa langue.
        def add_tag_to_typespermis(value):
            return self.add_tag_to(value, TagBase.TYPE_PERMIS)

        a = _('Licences')
        types_permis2 = TagTypedChoiceField(
            label=a, required=False,
            custom_tag=add_tag_to_typespermis,
            widget=forms.CheckboxSelectMultiple(attrs={
                'title':'test',
                'groupno': 3,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 6,
                'rowend': True}),
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
                'title':'test',
                'groupno': 3,
                'multiple': 'multiple',
                'class': 'form-group',
                'rowspan': 6,
                'rowstart': True, }),
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
                'title':'test',
                'groupno': 3,
                'rowspan': 6,
                'rowend': True,
                'multiple': 'multiple',
                'class': 'form-group'}),
            error_messages=self.e,
            choices=self.get_list_tags(TagBase.TYPE_LANGUE))

        # --------------------------------------------------------------------
        # Problème : self.fields est de type OrderedDict(), qui se base sur
        #            l'ordre d'ajout des éléments. Alors si on veut un autre
        #            ordre, pas d'autre choix que de reconstruire
        #            le dictionnaire en y appliquant l'ordre qu'on veut :
        new_fields = OrderedDict([
            ('field_picture', field_picture),
            ('field_picture_banner', field_picture_banner),
            ('user_first_name', user_first_name),
            ('user_last_name', user_last_name),
            ('email', self.fields['email']),
            ('sexe', self.fields['sexe']),
            ('field_place_i_live', field_place_i_live),
            ('date_naissance', self.fields['date_naissance']),
            # tant que pas premium :
            # ('statut', self.fields['statut']),
            ('field_place_of_birth', field_place_of_birth),
            ('langue', self.fields['langue']),
            ('how_did_i_know_cogofly', self.fields['how_did_i_know_cogofly']),
            ('nb_enfants', self.fields['nb_enfants']),

            ('langues2', langues2),
            ('niveau_etudes', self.fields['niveau_etudes']),

            ('programmes2', programmes2),

            ('field_employer_current', field_employer_current),
            ('field_employer_previous', field_employer_previous),
            ('profession', self.fields['profession']),

            ('activites2', activites2),
            ('hobbies2', hobbies2),
            ('types_permis2', types_permis2),
            ('personnalites2', personnalites2),

            ('est_fumeur', self.fields['est_fumeur']),
            ('custom_zodiac_sign', self.fields['custom_zodiac_sign']),

            # ('known_languages', known_languages),
            # ('types_permis', types_permis),
            # ('diplomes', diplomes),
            # ('centres_dinteret', centres_dinteret),
            ('self_description', self.fields['self_description']),
        ])
        for k, v in list(self.fields.items()):
            if not new_fields.get(k):  # (!) que s'ils n'y sont pas
                new_fields[k] = v

        self.fields = new_fields

    def clean_field_picture(self):
        retour = self.files.get('field_picture')
        if retour:
            try:
                retour = UploadedPictureHandler().encode_filename(retour,
                                                                  'profiles/',
                                                                  (400, 400),
                                                                  True)
                # (!) 2 types of exceptions : IOError and KeyError
                #     (PIL, PIL/Image.py line 1649 checks extension is ok):
            except (KeyError, IOError):
                retour = None
                self.errors['field_picture'] = \
                    ErrorList([_("Unknown type of image")])
        return retour

    def clean_field_picture_banner(self):
        retour = self.files.get('field_picture_banner')
        if retour:
            try:
                retour = UploadedPictureHandler().encode_filename(retour,
                                                                  'banners/',
                                                                  (400, 400))
                # (!) 2 types of exceptions : IOError and KeyError
                #     (PIL, PIL/Image.py line 1649 checks extension is ok):
            except (KeyError, IOError):
                retour = None
                self.errors['field_picture_banner'] =\
                    ErrorList([_("Unknown type of image")])
        return retour

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if not date_naissance:
            raise ValidationError(_('No birth date precised'))

        if relativedelta(datetime.datetime.now(), date_naissance).years < 18:
                raise ValidationError(_('Invalid birth date '
                                        '(you must be >= 18 years old)'))
        return date_naissance

    def clean(self):

        old = self.cleaned_data.get('old_password')
        new1 = self.cleaned_data.get('new_password1')
        new2 = self.cleaned_data.get('new_password2')
        if old:
            if not new1:
                raise ValidationError(_('New password missing'))
            if not new2:
                raise ValidationError(_('New password missing'))
            if new1 != new2:
                raise ValidationError(_("The new password "
                                        "is not the same twice"))
        # arrivé ici = on a bien rempli -> c'est dans la vue qu'on essaie de
        #                                  changer le mot de passe
        try:
            self.current_langue = Langue.objects.get(
                locale=translation.get_language())
        except Langue.DoesNotExist:
            # ne devrait jamais arriver, c'est géré dans le middleware :
            raise ValidationError(
                _("The language you've set is unknown ('{}'). "
                  "Please go to My Profile -> Change my parameters "
                  "and choose a known language").format(
                    translation.get_language()))

        return super(ProfileForm, self).clean()

    def is_valid(self):
        return super(ProfileForm, self).is_valid()

    def save(self, commit=True):

        place_of_birth = self.cleaned_data.get('field_place_of_birth')
        if place_of_birth:
            t = Tag.objects.create(
                type_tag=BaseTag.TYPE_GOOGLEMAPS,
                langue=self.current_langue,
                description=place_of_birth
            )
            t.save()
            self.instance.place_of_birth = t

        place_i_live = self.cleaned_data.get('field_place_i_live')
        if place_i_live:
            t = Tag.objects.create(
                type_tag=BaseTag.TYPE_GOOGLEMAPS,
                langue=self.current_langue,
                description=place_i_live
            )
            t.save()
            self.instance.place_i_live = t

        employer_current = self.cleaned_data.get('field_employer_current')
        if employer_current:
            t = Tag.objects.create(
                type_tag=BaseTag.TYPE_GOOGLEMAPS,
                langue=self.current_langue,
                description=employer_current
            )
            t.save()
            self.instance.employer_current = t

        employer_previous = self.cleaned_data.get('field_employer_previous')
        if employer_previous:
            t = Tag.objects.create(
                type_tag=BaseTag.TYPE_GOOGLEMAPS,
                langue=self.current_langue,
                description=employer_previous
            )
            t.save()
            self.instance.employer_previous = t

        retour = super(ProfileForm, self).save(commit)

        """
        (!!) Suppression des tags dynamiques sur demande de Franck,
             15 jours de boulot complets perdus / offerts mais c'est normal !!!
        def update_tags_with_value(tags, many_to_many_class, champ):
            if tags:
                many_to_many_class.objects.filter(
                    personne=self.instance,
                    date_v_fin=None
                ).update(date_v_fin=make_aware(django_datetime.now()))
                for idx_tag_with_value in tags:
                    args = {'personne': self.instance,
                            champ: TagWithValue.objects.get(
                                    pk=idx_tag_with_value
                            )}
                    pl = many_to_many_class.objects.create(**args)
                    pl.save()

        update_tags_with_value(self.cleaned_data.get('known_languages'),
                               PersonneLangue, 'langue')
        update_tags_with_value(self.cleaned_data.get('types_permis'),
                               PersonneTypePermis, 'type_permis')
        update_tags_with_value(self.cleaned_data.get('diplomes'),
                               PersonneDiplome, 'diplome')
        update_tags_with_value(self.cleaned_data.get('centres_dinteret'),
                               PersonneCentreDInteret, 'centre_dinteret')
        update_tags_with_value(self.cleaned_data.get('hobbies'),
                               PersonneHobby, 'hobby')
        """

        return retour
