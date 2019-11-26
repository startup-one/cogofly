# coding=UTF-8


import six.moves.urllib.request, six.moves.urllib.error, six.moves.urllib.parse

import ftfy
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from app.models.generic import BaseTranslatableModel, BaseModel, Langue
from six.moves.urllib.parse import urlencode
import json as simplejson
import six


class BaseTag(BaseTranslatableModel):
    TYPE_ENTREPRISE = '0'
    TYPE_PROFESSION = '1'
    TYPE_LANGUE = '2'
    TYPE_GOOGLEMAPS = '3'
    TYPE_PERMIS = '4'
    TYPE_DIPLOME = '5'
    TYPE_CENTRE_DINTERET = '6'
    TYPE_HOBBY = '7'
    TAB_TYPES = {
        TYPE_ENTREPRISE: _('Company'),
        TYPE_PROFESSION: _('Job'),
        TYPE_LANGUE: _('Language'),
        TYPE_GOOGLEMAPS: _('Google maps'),
        TYPE_PERMIS: _('Driving licences'),
        TYPE_DIPLOME: _('Diploma'),
        TYPE_CENTRE_DINTERET: _('Point of interest'),
        TYPE_HOBBY: _('Hobby'),
    }
    type_tag = models.CharField(max_length=1,
                                choices=[(a, b) for a, b in
                                         list(TAB_TYPES.items())],
                                default=TYPE_ENTREPRISE)

    class Meta(BaseModel.Meta):
        abstract = True


@python_2_unicode_compatible
class TagWithValue(BaseTag):
    description = models.CharField(max_length=200, default='', null=True,
                                   blank=True)
    value = models.CharField(max_length=200, default='', null=True,
                             blank=True)

    def __str__(self):
        return '{} - {} : {} -> {}'.format(
            self.id, self.langue.locale, self.description, self.value)

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Tag with an associated value")
        verbose_name_plural = _("Tags with an associated value")


@python_2_unicode_compatible
class Tag(BaseTag):
    description = models.CharField(max_length=200, default='', null=True,
                                   blank=True)

    def __str__(self):
        return self.description

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Tag")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOUVELLE RÉECRITURE
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOUVELLE RÉECRITURE
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NOUVELLE RÉECRITURE
@python_2_unicode_compatible
class TagBase(BaseModel):
    TYPE_MATIERE = 1
    TYPE_ACTIVITE = 2
    TYPE_HOBBY = 3
    TYPE_PERMIS = 4
    TYPE_PERSONNALITE = 5
    TYPE_LANGUE = 6
    TYPE_GOOGLE_MAP = 7
    TAB_TYPES = {
        TYPE_MATIERE: _('Subjects'),
        TYPE_ACTIVITE: _('Activity sectors'),
        TYPE_HOBBY: _('Hobbies'),
        TYPE_PERMIS: _('Driving licences'),
        TYPE_PERSONNALITE: _('Personality'),
        TYPE_LANGUE: _('Language'),
        TYPE_GOOGLE_MAP: _('Google maps'),
    }
    type_tag = models.IntegerField(choices=[(a, b) for a, b in
                                            list(TAB_TYPES.items())],
                                   null=True, blank=True,
                                   default=None)
    poids = models.IntegerField(default=None, blank=True, null=True,
                                help_text=_("Used for ordering"),)
    description = models.CharField(max_length=200, default='', null=True,
                                   blank=True)

    def __str__(self):
        return '({}) - {}'.format(
            TagBase.TAB_TYPES[self.type_tag] if self.type_tag else '?',
            self.description)

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Referent tag")
        verbose_name_plural = _("Referent tags")


@python_2_unicode_compatible
class TagTraduit(BaseModel):
    tag = models.ForeignKey(TagBase, default=None, on_delete=models.CASCADE,blank=True, null=True,
                            help_text=_("It's the master tag"),
                            related_name='tag')
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE, default=None, blank=True, null=True)
    value = models.CharField(max_length=200, default='', null=True,
                             blank=True)

    def __str__(self):
        return '{} - {} ({}) -> {}'.format(
            self.id,
            str(self.tag) if self.tag else '(?)',
            self.langue.locale if self.langue else '(?)',
            self.value)

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Tag translated from a referent tag")
        verbose_name_plural = _("Tags translated")


@python_2_unicode_compatible
class TagGoogleMaps(TagBase):
    place_id = models.CharField(max_length=100, default='', null=True,
                                blank=True)

    lat = models.DecimalField(default=None, null=True, blank=True,
                              max_digits=19, decimal_places=10)

    lng = models.DecimalField(default=None, null=True, blank=True,
                              max_digits=19, decimal_places=10)

    # https://developers.google.com/maps/documentation/
    # geocoding/intro?hl=fr#Results
    # viewport contient la fenêtre d'affichage recommandée pour
    # l'affichage du résultat renvoyé, spécifié sous la forme de deux valeurs
    # latitude,longitude définissant les angles southwest et northeast de
    # la zone de délimitation de la fenêtre d'affichage.
    # La fenêtre d'affichage est généralement utilisée pour encadrer un
    # résultat présenté à l'utilisateur.
    viewport_northeast_lat = models.DecimalField(default=None, null=True,
                                                 blank=True,
                                                 max_digits=19,
                                                 decimal_places=10)
    viewport_northeast_lng = models.DecimalField(default=None, null=True,
                                                 blank=True,
                                                 max_digits=19,
                                                 decimal_places=10)
    viewport_southwest_lat = models.DecimalField(default=None, null=True,
                                                 blank=True,
                                                 max_digits=19,
                                                 decimal_places=10)
    viewport_southwest_lng = models.DecimalField(default=None, null=True,
                                                 blank=True,
                                                 max_digits=19,
                                                 decimal_places=10)

    def __str__(self):
        return _('{} (lat: {}, lng: {})').format(
            self.description,
            self.lat if self.lat else '?', self.lng if self.lng else '?')

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Tag google maps referent")
        verbose_name_plural = _("Tags google maps referents")


class GoogleException(Exception):
    pass


@python_2_unicode_compatible
class TagGoogleMapsTraduit(BaseModel):
    tag_google_maps = models.ForeignKey(
        TagGoogleMaps, default=None, blank=True, null=True,
        help_text=_("Position de référence"),
        related_name='tag_google_maps', on_delete=models.CASCADE)
    langue = models.ForeignKey(Langue, default=None, blank=True, null=True, on_delete=models.CASCADE)
    # formatted_address selon les langues :
    # 'en' : "Beijing, Beijing, China", 'fr' : "P\u00e9kin, P\u00e9kin, Chine"
    formatted_address = models.CharField(max_length=200, default='', null=True,
                                         blank=True)

    # GMAPS_URL = 'http://maps.google.com/maps/api/geocode/json'
    # (!) url d'auto complete pour avoir des SUGGESTIONS google :
    # GMAPS_URL = u'https://' \
    #             u'maps.googleapis.com/maps/api/place/autocomplete/json'
    # (!) url pour chercher des places existantes :
    GMAPS_URL = 'https://maps.googleapis.com/maps/' \
                'api/place/textsearch/json'

    @staticmethod
    def make_cache_via_google_maps(text, locale):
        # Deux exemples pour mémo, à supprimer quand code fini :
        #
        # geocode(self, {                      geocode(self, {
        #     'input': u'Beijing, China',          'input': u'Pékin, Chine',
        #     'language': u'en',                   'language': u'fr',
        # })                                   })
        geo_args = {
            'input': text,
            'language': locale,
            # clé cogofly, compte cogofly@gmail.com, projet cogofly :
            # clé *Serveur* ne fonctionne pas :
            # 'key': u'AIzaSyC-05bQU8KfMuvr23-VmqROV_OKGizhdiM'
            # clé *Client* fonctionne :
            'key': 'AIzaSyCc0zrgx2mk-YPqzUvvpv4anNNWbMMk9EQ'

        }
        # Tout convertir en unicode
        str_geo_args = {}
        for k, v in six.iteritems(geo_args):
            str_geo_args[k] = ftfy.fix_encoding(six.text_type(v)).encode('utf-8')

        url = TagGoogleMapsTraduit.GMAPS_URL + '?' + urlencode(str_geo_args)
        print(url)
        request = six.moves.urllib.request.Request(url, headers={
            # "Referer": "http://www.cogofly.com/",
            "Referer": "http://cogofly.com",
            "userIp": "62.210.178.49"
        })
        print(request)
        handle = six.moves.urllib.request.urlopen(request).read()
        result = simplejson.loads(handle)
        print('src')
        print(geo_args)
        print('result')
        print((simplejson.dumps(result, indent=4)))

        print(("result['status'] -> {}".format(result['status'])))
        # "OK"               indique qu'aucune erreur n'est survenue, que
        #                    l'adresse a été analysée et qu'au moins un
        #                    géocode a été trouvé.
        # "ZERO_RESULTS"     indique que le géocode a réussi mais n'a renvoyé
        #                    aucun résultat. Cela peut se produire si le
        #                    géocodeur a reçu un paramètre address inexistant.
        # "OVER_QUERY_LIMIT" indique que vous avez dépassé votre quota.
        # "REQUEST_DENIED"   indique que votre requête a été rejetée.
        # "INVALID_REQUEST"  indique généralement qu'il manque un élément
        #                    (address, components ou latlng) de la requête.
        # "UNKNOWN_ERROR"    indique que la requête n'a pas pu être traitée
        #                    en raison d'une erreur de serveur.
        #                    Si vous essayez à nouveau, la requête pourrait
        #                    aboutir.
        if result['status'] == "REQUEST_DENIED":
            # RAF : envoyer un mail
            raise Exception(_("We have a technical error. "
                              "Please try again."))

        # Si même google trouve pas on arrête tout :
        if not len(result['results']):
            raise GoogleException(_("Google didn't find a town/country "
                                    "with this name"))

        # 1 - aller chercher si on l'a en base :
        tag = None
        formatted_address = None
        for place in result['results']:
            try:
                tag = TagGoogleMaps.objects.get(
                    place_id__exact=place['place_id'])
                formatted_address = place.get('formatted_address')
            except TagGoogleMaps.DoesNotExist:
                pass
        if tag is None:
            # Prendre le premier résultat qui est souvent le bon
            place = result['results'][0]
            formatted_address = place.get('formatted_address')
            description = place.get('name', _('No name from google maps'))
            # Pas trouvé en base, créer position référence = TagGoogleMaps
            if not place.get('geometry'):  # devrait jamais arriver :
                raise GoogleException(_("Google didn't provide a location for "
                                        "this town/country with this name"))

            def _g(tab, args):
                print(tab, args)
                if tab.get(args[0]) is None:
                    return None
                if len(args) > 1:
                    return _g(tab[args[0]], args[1:])
                return tab.get(args[0])
            g = place['geometry']
            tag = TagGoogleMaps.objects.create(
                type_tag=TagBase.TYPE_GOOGLE_MAP,
                description=description,
                place_id=place['place_id'],
                lat=_g(g, ['location', 'lat']),
                lng=_g(g, ['location', 'lng']),
                viewport_northeast_lat=_g(g, ['viewport', 'northeast', 'lat']),
                viewport_northeast_lng=_g(g, ['viewport', 'northeast', 'lng']),
                viewport_southwest_lat=_g(g, ['viewport', 'southwest', 'lat']),
                viewport_southwest_lng=_g(g, ['viewport', 'southwest', 'lng']),
            )
            tag.save()

        # arrivé ici, tag vaut forcément quelque chose
        # Si on a appelé cette fonction en cours, c'est que TagGoogleMapsTraduit
        # n'avait pas renvoyé d'enregistrement
        # -> le créer et le renvoyer
        tt = TagGoogleMapsTraduit.objects.create(
            tag_google_maps=tag,
            langue=Langue.objects.get(locale__exact=locale),
            # formatted_address selon les langues :
            # 'en' : "Beijing, Beijing, China",
            # 'fr' : "P\u00e9kin, P\u00e9kin, Chine"
            formatted_address=formatted_address)
        tt.save()
        if text != formatted_address:
            # Le texte entré par l'utilisateur n'est pas le même que le retour
            # google, enregistrer les deux :
            tt = TagGoogleMapsTraduit.objects.create(
                tag_google_maps=tag,
                langue=Langue.objects.get(locale__exact=locale),
                formatted_address=text)
            tt.save()
        return tt
        # Infos que je n'ai pas gardé en cache (inutiles ici)
        # "results": [
        #     {
        #         "name": "Paris",
        #         "reference": "Cn... blabla on s'en fout...bpn8",
        #         "types": [
        #             "locality",
        #             "political"
        #         ],
        #         "icon": "url image d'une pin pour pointer"
        #     }
        # ]

    def __str__(self):
        return '{} - {} ({}) -> {}'.format(
            self.id,
            str(self.tag_google_maps) if self.tag_google_maps else '(?)',
            self.langue.locale if self.langue else '(?)',
            self.formatted_address)

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Tag google maps of a place in a language")
        verbose_name_plural = _("Tags google maps of a place in a language")
