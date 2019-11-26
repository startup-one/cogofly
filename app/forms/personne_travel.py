# coding=UTF-8


from collections import OrderedDict

from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, \
    MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.forms import widgets
from django.forms.utils import ErrorList
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from app.forms.generic import FormFieldDatePartial
from app.forms.generic.fields.custom_image_field import CustomImageField
from app.forms.generic.generic import FormForceLocalizedDateFields, \
    UploadedPictureHandler
from app.forms.widgets.google_maps import GoogleMapsWidget
from app.forms.widgets.widget_date_selector import DateSelectorWidget
from app.models.generic import Langue, PictureURL
from app.models.tag import TagWithValue, BaseTag, TagGoogleMapsTraduit, \
    GoogleException
from app.models.personne import PersonneTravel, Photo


class PersonneTravelForm(FormForceLocalizedDateFields):

    class Meta:
        model = PersonneTravel
        exclude = ('personne', 'travel', 'date_start', 'date_end', 'comments',
                   'date_v_debut', 'date_v_fin',
                   'ignore_start_dd', 'ignore_start_mm',
                   'ignore_end_dd', 'ignore_end_mm',
                   'photo1', 'photo2', 'photo3',)

    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('Town / Country / Place:')
    travel = forms.CharField(
        # (!) laisser required=False, je le gère plus loin s'il est vide :
        label=a, max_length=100, required=False,
        widget=GoogleMapsWidget(attrs={
            'title': a, 'size': 100, 'type': 'text',
            'rowstart': True,
            'rowspan': 12,
            'rowend': True,
            'placeholder': _('town / country / place'),
            'class': 'form-control'}),
        error_messages=e)

    a = _('Start:')
    date_start = FormFieldDatePartial(
        label=a, localize=True, required=False,
        widget=DateSelectorWidget(attrs={
            'title': a,
            'rowstart': True,
            'rowspan': 6,
            'style': "display: inline-block; width: auto",
            'class': 'form-control'}))

    a = _('End:')
    date_end = FormFieldDatePartial(
        label=a, localize=True, required=False,
        widget=DateSelectorWidget(attrs={
            'title': a,
            'rowspan': 6,
            'rowend': True,
            'style': "display: inline-block; width: auto",
            'class': 'form-control'}))

    a = _('Add a comment:')
    comments = forms.CharField(
        label=a, localize=True, required=False,
        widget=widgets.Textarea(attrs={
            'title': a,
            'rows': 5, 'cols': 40, 'style': 'resize: vertical',
            'rowstart': True,
            'rowspan': 6,
            'rowend': True,
            'class': 'form-control'}))

    is_past = forms.BooleanField(required=False,
                                 widget=widgets.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(PersonneTravelForm, self).__init__(*args, **kwargs)
        kw = kwargs.get('initial')

        # I've made a CustomImageField to be able to pass custom parameters
        # 'picture_attributes' where I put infos on the image so I can easily
        # display the image in the template through "field.picture_attributes":
        def local_creer_custom_image_field(idx):
            img = None
            if kw:
                photo = kw.get('field_photo_{}'.format(idx))
                if photo:
                    img = str(photo.url())
            if not img:  # url vide = image d'une photo vide
                img = PictureURL.get_url()
            l_a = _('Picture {}:').format(idx)
            return CustomImageField(
                label=l_a, allow_empty_file=True, required=False,
                help_text=None if idx > 1 else
                _("<span class=\"suggestion\">"
                  "Want to upload photos of your different experiences and "
                  "inspire future travellers?</span>"),
                picture_attributes={
                    'width': 'auto', 'height': 100,
                    'style': 'margin:10px; ',
                    'url': img
                },
                widget=forms.FileInput(attrs={
                    'title': l_a,
                    'rowstart': True,
                    'rowspan': 12,
                    'rowend': True,
                    'placeholder': _('picture {}').format(idx),
                    'class': 'form-control travel-image',
                    'accept': "image/*", }),
                error_messages=self.e)

        field_photo_1 = local_creer_custom_image_field(1)
        field_photo_2 = local_creer_custom_image_field(2)
        field_photo_3 = local_creer_custom_image_field(3)

        # --------------------------------------------------------------------
        # Problème : self.fields est de type OrderedDict(), qui se base sur
        #            l'ordre d'ajout des éléments. Alors si on veut un autre
        #            ordre, pas d'autre choix que de reconstruire
        #            le dictionnaire en y appliquant l'ordre qu'on veut :
        new_fields = OrderedDict([
            ('travel', self.fields['travel']),
            ('date_start', self.fields['date_start']),
            ('date_end', self.fields['date_end']),
            ('comments', self.fields['comments']),
            ('field_photo_1', field_photo_1),
            ('field_photo_2', field_photo_2),
            ('field_photo_3', field_photo_3),
        ])
        # Des fois, je construis la forme "manuellement" en lui envoyant
        # directement les champs dans un dict() PersonneTravelForm({ info })
        # Tous les champs passés sont ceux attendus, mais EN PLUS
        # j'y ajoute le pk comme ça dans mon code, si je vois que le
        # pk est présent, c'est une édition de la forme et je fais un update
        if len(args):
            if 'pk' in args[0]:
                new_fields['pk'] = forms.IntegerField(
                        widget=widgets.HiddenInput())
        elif kw:
            if kw.get('pk'):
                new_fields['pk'] = forms.IntegerField(
                        widget=widgets.HiddenInput())
        elif kwargs.get('data'):
            pk = kwargs.get('data').get('pk')
            if pk:
                # pk revenu dans le post = cf long commentaire au dessus
                new_fields['pk'] = forms.IntegerField(
                        widget=widgets.HiddenInput())

        for kw, v in list(self.fields.items()):
            if not new_fields.get(kw):  # (!) que s'ils n'y sont pas
                new_fields[kw] = v

        self.fields = new_fields

    def handle_uploaded_photos(self, field):
        original, final = self.files.get(field), None
        if original:
            try:
                final = UploadedPictureHandler().encode_filename(original,
                                                                 'travels/')
                return Photo.objects.create(fichier_origine=original,
                                            image=final)
            except IOError:
                self.errors[field] = ErrorList([_("Unknown type of image")])
        return None

    def clean_field_photo_1(self):
        return self.handle_uploaded_photos('field_photo_1')

    def clean_field_photo_2(self):
        return self.handle_uploaded_photos('field_photo_2')

    def clean_field_photo_3(self):
        return self.handle_uploaded_photos('field_photo_3')

    def clean_date_start(self):
        # Je ne sais pas comment remonter l'erreur via mon widget custom
        # car l'erreur est levée au niveau d'un DatePartial, je l'ai donc
        # gardée dans un tableau "errors" que je vérifie ici :
        if len(self.fields['date_start'].widget.errors):
            raise ValidationError(
                _(self.fields['date_start'].widget.errors[0]))
        return str(self.fields['date_start'].widget.date_partial)

    def clean_travel(self):
        travel = self.cleaned_data['travel']
        if travel == '':
            return None
        langue = Langue.objects.get(locale__exact=translation.get_language())
        locale = langue.locale
        try:
            retour = TagGoogleMapsTraduit.objects.get(
                langue__locale__exact=locale,
                formatted_address__iexact=travel
            )
        except MultipleObjectsReturned:
            # Garder le plus long ()
            retour = None
            for a in TagGoogleMapsTraduit.objects.filter(
                            langue__locale__exact=locale,
                            formatted_address__iexact=travel):
                if retour:
                    # Si des min et des maj c'est sûrement un retour google
                    if any(x.isupper() for x in str(a)) and \
                            any(x.islower() for x in str(a)):
                        # Si il est le plus long
                        if len(retour.formatted_address) < \
                                len(a.formatted_address):
                            # Min/maj + plus long -> on le garde
                            retour = a
                else:
                    retour = a
        except TagGoogleMapsTraduit.DoesNotExist:
            try:
                retour = TagGoogleMapsTraduit.make_cache_via_google_maps(
                    text=travel, locale=locale)
            except GoogleException as e:
                raise ValidationError(e.message)
        return retour

    def clean_pk(self):
        try:
            return int(self.cleaned_data['pk'])
        except ValueError:
            return None

    def clean(self):
        # print(self.cleaned_data)
        # Arrivé ici c'est après tous les appels à clean_XXX où XXX = champ du
        # formulaire. Ici on est censé faire une vérification "globale", c'est
        # à dire une vérification qui ne concerne pas un champ en particulier.
        return super(PersonneTravelForm, self).clean()
