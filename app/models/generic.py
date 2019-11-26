# coding=UTF-8

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.templatetags import staticfiles
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import date_format
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.dateformat import DateFormat
from django.urls import reverse_lazy
from django.utils import timezone


class PictureURL(object):
    """
    Classe pour récuperer l'URL d'une image, ou l'URL par défaut si image vide
    """
    @staticmethod
    def get_url(img=None, default=None):
        if img:
            return reverse_lazy('url_public', args=(img.name[2:]
                                                    if img.name.startswith('./')
                                                    else img.name,))
        if default:
            return staticfiles.static(default)
        return staticfiles.static('img/no-image-yet.jpg')


class ObjectsStillValidManager(models.Manager):
    def still_valid(self):
        return self.get_queryset().filter(date_v_fin__exact=None)

    def still_valid_distinct(self):
        return self.get_queryset().filter(date_v_fin__exact=None).distinct()


class BaseModel(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True,
                                         verbose_name=_('Created'))
    date_last_modif = models.DateTimeField(auto_now=True,
                                           verbose_name=_('Last changed'))
    date_v_debut = models.DateTimeField(
        default=timezone.now,
        editable=True,
        verbose_name=_("V. start")
    )
    date_v_fin = models.DateTimeField(
        default=None,
        null=True,
        editable=True,
        verbose_name=_("V. end"),
        blank=True
    )
    objects = ObjectsStillValidManager()

    @staticmethod
    def format_date(value):
        return DateFormat(value).format('d/m/Y, H:i') if value else _('Infini')

    @staticmethod
    def to_str(value, default='?'):
        return str(value) if value else default

    """
    Sur http://stackoverflow.com, solution pour ajouter un champ en lecture
    seule qui affiche l'image d'un champ de type models.ImageField() :
    /questions/16307307/django-admin-show-image-from-imagefield
    Seul hic, mais ça convient pour l'instant à mes besoins : il va chercher
    une propriété en dur. Moi je l'ai bêtement nommé propriété "image".
    """
    def image_tag(self):
        if self.image:
            return '<img src="{0}" ' \
                   'style="width:200px; height:auto;"s/>'.format(
                       reverse_lazy('url_public', args=(self.image,))
                   )
        else:
            return _('(Empty)')

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    @staticmethod
    def date_relative(d, most_recent=None):
        if d is None:
            return _('No date')
        if most_recent is None:
            diff = now() - d
        else:
            diff = most_recent - d
        s = diff.seconds
        if diff.days > 7 or diff.days < 0:
            if d.year == now().year:
                return date_format(d, 'MONTH_DAY_FORMAT', use_l10n=True)
            return date_format(d, 'SHORT_DATE_FORMAT', use_l10n=True)
        elif diff.days == 1:
            return _("1 day ago")
        elif diff.days > 1:
            return _("{} days ago").format(diff.days)
        elif s <= 1:
            return _("Just now")
        elif s < 60:
            return _("{} seconds ago").format(s)
        elif s < 120:
            return _("1 minute ago")
        elif s < 3600:
            return _("{} minutes ago").format(s / 60)
        elif s < 7200:
            return _("1 hour ago")
        else:
            return _("{} hours ago").format(s / 3600)

    def date_creation_relative(self):
        return self.date_relative(self.date_creation)

    class Meta:
        abstract = True
        ordering = ['date_v_debut']


class ManyToManyStillValid(models.ManyToManyField):

    def all_valid(self):
        return self.all().filter(date_v_fin__null=True)


@python_2_unicode_compatible
class Langue(BaseModel):
    nom = models.CharField(max_length=50)
    nom_local = models.CharField(max_length=50, default='')
    locale = models.CharField(max_length=2)  # (e.g. "fr")
    bidirectionnel = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def url_drapeau(self):
        if not self.locale:
            return None
        # path codé en dur, ça ne devrait jamais changer :
        a = 'img/flags/flag-{}-s.png'.format(self.locale)
        # ! Astuce : finder de django :
        if not finders.find(a):
            return None
        return staticfiles.static(a)

    def __str__(self):
        return '{} / {}{}'.format(
            self.locale, self.nom, (_("- activated") if self.active else "")
        )

    class Meta(BaseModel.Meta):
        verbose_name_plural = _("Languages")


class BaseTranslatableModel(BaseModel):
    langue = models.ForeignKey(Langue, on_delete=models.PROTECT)

    class Meta(BaseModel.Meta):
        abstract = True


@python_2_unicode_compatible
class Texte(BaseTranslatableModel):
    texte = models.CharField(max_length=200)

    def __str__(self):
        return self.texte

    class Meta(BaseTranslatableModel.Meta):
        verbose_name = _("Text")


