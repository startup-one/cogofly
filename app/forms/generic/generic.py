# coding=UTF-8

import os
import uuid

import datetime
from os.path import splitext, basename, abspath, join

import PIL
from PIL import ExifTags
from PIL import Image
from django import forms
from django.forms import widgets
from django.utils import formats, translation

from app.models.generic import Langue
from app.models.tag import TagWithValue, TagTraduit
from cogofly.settings import MEDIA_ROOT


class UploadedPictureHandler(object):

    @staticmethod
    def get_url(name, path=None):
        retour = (path if path else '') + name
        # Ex: "profiles/bea536a0/089c/a45b.jpg"
        return retour.replace('-', '/')

    @staticmethod
    def compute_url_fullsize(name, path=None):
        # -> dst  : "profiles/full/bea536a0-089c-a45b.jpg"
        return UploadedPictureHandler.get_url(name,
                                              (path if path else '') +
                                              'full/')

    @staticmethod
    def compute_url_thumbnail(name, path=None):
        # -> dst  : "profiles/th/bea536a0-089c-a45b.jpg"
        return UploadedPictureHandler.get_url(name,
                                              (path if path else '') +
                                              'th/')

    @staticmethod
    def encode_filename(uploaded_file, path_dest=None,
                        thumbnail_dimensions=(), return_thumbnail=False):

        # pris ici : http://stackoverflow.com/questions/
        # 6999726/how-can-i-convert-a-datetime-object-to
        # -milliseconds-since-epoch-unix-time-in-p
        #
        epoch = datetime.datetime.utcfromtimestamp(0)

        def millis(dt):
            return (dt - epoch).total_seconds() * 1000.0

        img = Image.open(uploaded_file)
        try:
            # rotation img code
            for orientation in list(ExifTags.TAGS.keys()):
                if ExifTags.TAGS[orientation] == 'Orientation':
                    try:
                        exif = dict(list(img._getexif().items()))
                        if exif[orientation] is 6:
                            img = img.rotate(-90, expand=True)
                        elif exif[orientation] is 8:
                            img = img.rotate(90, expand=True)
                        elif exif[orientation] is 3:
                            img = img.rotate(180, expand=True)
                        elif exif[orientation] is 2:
                            img = img.transpose(
                                Image.FLIP_LEFT_RIGHT, expand=True)
                        elif exif[orientation] is 5:
                            img = img.rotate(-90).transpose(
                                Image.FLIP_LEFT_RIGHT, expand=True)
                        elif exif[orientation] is 7:
                            img = img.rotate(90, expand=True).transpose(
                                Image.FLIP_LEFT_RIGHT, expand=True)
                        elif exif[orientation] is 4:
                            img = img.rotate(180).transpose(
                                Image.FLIP_LEFT_RIGHT, expand=True)
                        break
                    except ZeroDivisionError:
                        # error unknown due to PIL/TiffImagePlugin.py buggy
                        # -> ignore this "rotation img" code, just continue
                        break
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            # -> ignore this "rotation img" code, just continue
            pass
        nom = str(int(millis(datetime.datetime.now())))
        nom = str(uuid.uuid5(uuid.NAMESPACE_OID,
                             nom.encode('utf-8'))) + \
            splitext(basename(uploaded_file.name))[1]

        # Ex: "profiles/bea536a0-089c-a45b.jpg"
        # -> dst  : "profiles/full/bea536a0-089c-a45b.jpg"
        # -> thumb: "profiles/th/bea536a0-089c-a45b.jpg"
        dst = UploadedPictureHandler.compute_url_fullsize(nom, path_dest)
        dst_thumbnail = UploadedPictureHandler.compute_url_thumbnail(nom,
                                                                     path_dest)

        # Ex: "C:\Users\...\uploads\profiles\full\bea536a0\089c\a45b.jpg"
        dst_full = abspath(join(MEDIA_ROOT, dst))
        dst_full_thumbnail = abspath(join(MEDIA_ROOT, dst_thumbnail))

        # Ex: "C:\Users\...\uploads\profiles"
        dst_base = os.path.dirname(dst_full)
        if not os.path.exists(dst_base):
            os.makedirs(dst_base, 0o777)

        dst_base = os.path.dirname(dst_full_thumbnail)
        if not os.path.exists(dst_base):
            os.makedirs(dst_base, 0o777)

        img.save(dst_full)
        if len(thumbnail_dimensions) == 2:
            w_thumbnail, h_thumbnail = thumbnail_dimensions
            percent = min(w_thumbnail / float(img.size[0]),
                          h_thumbnail / float(img.size[1]))
            img = img.resize((int(float(img.size[0])*percent),
                              int(float(img.size[1])*percent)),
                             PIL.Image.ANTIALIAS)
            img.save(dst_full_thumbnail)
            if return_thumbnail:
                return dst_thumbnail

        # everything ok -> return only filename
        return dst


class SpecialTagTypedChoiceField(object):
        # # --------------------------------------------------------------------
        # # Routines génériques pour les champs qui sont super particuliers :
        # # ils peuvent soit demander via JSON et aider l'utilisateur à choisir
        # # parmi une liste retournée du JSON, soit *ajouter* ce qu'a tapé
        # # l'utilisateur si ça ne fait pas partie de la liste :
        # # (!) Ca risque d'être lourd si le site décolle vraiment.
        # # --> Voir aussi get_initial() de la vue qui pré-remplit le champ
        # @staticmethod
        # def add_tag_to(value, type_t):
        #     current_language = translation.get_language()
        #     t = TagWithValue.objects.create(
        #         langue=Langue.objects.get(locale__exact=current_language),
        #         type_tag=type_t,
        #         description=current_language,
        #         value=value,
        #     )
        #     return t.pk

        # @staticmethod
        # def get_list_tags(type_tag):
        #     a = TagWithValue.objects.filter(
        #         # langue__locale__exact=translation.get_language(),
        #         type_tag__exact=type_tag
        #     ).values_list('pk', 'value')
        #     print a
        #     return a

        # --------------------------------------------------------------------
        # Franck m'a demandé de détruire mes 10 jours et nuits de boulot pour
        # réussir à faire ce que j'ai fait au dessus, et cela s'est transformé
        # ainsi :
        @staticmethod
        def add_tag_to(value, type_t):
            current_language = translation.get_language()
            t = TagWithValue.objects.create(
                langue=Langue.objects.get(locale__exact=current_language),
                type_tag=type_t,
                description=current_language,
                value=value,
            )
            return t.pk

        @staticmethod
        def get_list_tags(type_tag):
            return TagTraduit.objects.filter(
                langue__locale__exact=translation.get_language(),
                tag__type_tag__exact=type_tag
            ).order_by('tag__poids', 'value').values_list('pk', 'value')


class FormForceLocalizedDateFields(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormForceLocalizedDateFields, self).__init__(*args, **kwargs)
        # Le principe : la traduction de Django... en anglais est un problème !
        # Le format appliqué en fonction de la langue courante par défaut
        # est le premier du tableau formats.get_format('DATE_INPUT_FORMATS')
        # ...codé en dur dans la classe DateTimeBaseInput :
        # -> rechercher la fonction _format_value()
        # Bref. Par défaut, le format international anglais
        # renvoie "Y-m-d", au lieu de "m/d/Y". Soit j'ai loupé quelque chose,
        # soit c'est du n'importe quoi.
        # Mais en regardant de plus près le deuxième item du tableau
        # 'DATE_INPUT_FORMATS', je vois qu'il est pour toutes les langues
        # presque sur le même principe du genre "d/m/y" ou  "m/d/y".
        # Donc je hacke : dans le constructeur, les widgets sont déjà crées,
        # donc je force à la main les widgets de type DateInput qui sont
        # localisés ET qui n'ont pas de format spécifique assigné.
        # Hack à supprimer le jour le core de Django a corrigé cela :
        force = formats.get_format('DATE_INPUT_FORMATS')[1]
        for k, v in list(self.fields.items()):
            if isinstance(v.widget, widgets.DateInput):
                # si date localisé SANS format, alors surcharger :
                if getattr(v, 'localize', False):
                    if not getattr(v.widget, 'format', None):
                        v.widget.format = force


