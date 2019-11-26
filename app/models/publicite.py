# coding=UTF-8

import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_markdown.models import MarkdownField

from app.models.generic import BaseModel


@python_2_unicode_compatible
class Publicite(BaseModel):

    PUBLICITE_VOYAGES_DROITE = 1
    PUBLICITE_VOYAGES_GAUCHE = 2
    PUBLICITE_MY_PROFILE_GAUCHE = 3
    PUBLICITE_MY_PROFILE_DROITE = 4
    PUBLICITE_FIL_ACTUALITE_GAUCHE = 5
    PUBLICITE_FIL_ACTUALITE_DROITE = 6

    TAB_PUBLICITE = {
        PUBLICITE_VOYAGES_DROITE: _('Ads travels right'),
        PUBLICITE_VOYAGES_GAUCHE: _('Ads travels left'),
        PUBLICITE_MY_PROFILE_GAUCHE: _('Ads my profile left'),
        PUBLICITE_MY_PROFILE_DROITE: _('Ads my profile right'),
        PUBLICITE_FIL_ACTUALITE_GAUCHE: _('Ads news left'),
        PUBLICITE_FIL_ACTUALITE_DROITE: _('Ads news right'),
    }

    position = models.IntegerField(
        choices=[(a, b) for a, b in list(TAB_PUBLICITE.items())],
        default=None, null=True, blank=True,
        help_text=_("Where this ads goes"),
        verbose_name=_("Where this ads goes"), )

    label = models.CharField(default=None, null=True, blank=True,
                             max_length=200,
                             help_text=_("A recall of what this ads "
                                         "contains (language independant)"),
                             verbose_name=_('Label'),)
    date_publication = models.DateTimeField(default=datetime.datetime.now,
                                            null=True, blank=True,
                                            verbose_name=_('Publication date'))
    ordre_si_top = models.IntegerField(
        null=True, blank=True, default=None,
        help_text=_('Priority: the lowest the higher '
                    '("1" is <b>before</b> "2" and so on...).'),
        verbose_name=_('How this ad appears'))

    def __str__(self):
        if not self.label:
            return ''
        return (self.label[:95] + '...') if len(self.label) > 90 else self.label

    class Meta(BaseModel.Meta):
        ordering = ['date_v_debut']
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')


@python_2_unicode_compatible
class PubliciteTraduit(BaseModel):
    publicite = models.ForeignKey(Publicite, default=None, null=True,
                                  blank=True, on_delete=models.CASCADE)
    locale = models.CharField(default=None, null=True, blank=True,
                              max_length=2,
                              help_text=_("Ads locale (en, fr, ...)"),
                              verbose_name=_("Ads locale"),)
    title = models.CharField(default=None, null=True, blank=True,
                             max_length=200,
                             help_text=_("Ads title"),
                             verbose_name=_('Title'),)
    content = MarkdownField(default=None, null=True, blank=True,
                            help_text=_("Ads content"),
                            verbose_name=_('Content'),)

    def description(self):
        a = '{} / {} - {}'.format(
            self.locale if self.locale else _('no locale'),
            self.title if self.locale else _('no title'),
            self.content if self.content else _('no content yet'),)
        return (a[:95] + '...') if len(a) > 90 else a

    def __str__(self):
        return self.description().strip()

    class Meta(BaseModel.Meta):
        ordering = ['date_v_debut']
        verbose_name = _('Ads-translated content')
        verbose_name_plural = _('Ads-translated')
