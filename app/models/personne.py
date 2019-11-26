# coding=UTF-8



import datetime
from itertools import chain
from bisect import bisect

from django.urls import reverse_lazy
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q, Count
from django.utils import formats
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import date_format, get_format
from django.utils.functional import cached_property
from django.utils.html import MLStripper
from django.utils.timezone import make_aware
from django.utils.translation import ugettext_lazy as _, ungettext, pgettext
from django.contrib.auth.models import User
from django.db import models

from app.models.blog import Blog, BlogTraduit
from app.models.date_partial_field import DatePartialField
from app.models.generic import BaseModel, PictureURL, ManyToManyStillValid, \
    Langue
from app.models.tag import Tag, TagTraduit, TagGoogleMapsTraduit
from app.models.personne_enums import PersonneEnums


@python_2_unicode_compatible
class Photo(PictureURL, BaseModel):

    fichier_origine = models.CharField(
        max_length=200, default=None, null=True, blank=True,
        help_text=_("It's filled when someone adds a trip picture, "
                    "you should not touch it"))
    image = models.ImageField(null=True)

    def url(self, default=None):
        return self.get_url(self.image, default)

    def __str__(self):
        return '{}'.format(self.image)


@python_2_unicode_compatible
class Personne(PictureURL, BaseModel):

    def __init__(self, *args, **kwargs):
        # Mise en place de cache :
        self.cache = {}
        super(Personne, self).__init__(*args, **kwargs)

    site_web = models.CharField(max_length=200,
                                default=None, blank=True, null=True)
    site_language = models.ForeignKey(Langue, null=True, on_delete=models.CASCADE,
                                      default=None, blank=True,
                                      related_name='site_language',
                                      verbose_name=_('Language chosen '
                                                     'in the website'))
    # (!) Rien en base de données, pour le signe du zodiaque, c'est calculé
    #     dynamiquement !
    ZODIAC_SIGNS = [(1, 20, _('Capricorn')),
                    (2, 18, _('Aquarius')),
                    (3, 20, _('Pisces')),
                    (4, 20, _('Aries')),
                    (5, 21, _('Taurus')),
                    (6, 21, _('Gemini')),
                    (7, 22, _('Cancer')),
                    (8, 23, _('Leo')),
                    (9, 23, _('Virgo')),
                    (10, 23, _('Libra')),
                    (11, 22, _('Scorpio')),
                    (12, 22, _('Sagittarius')),
                    (12, 31, _('Capricorn'))]

    def zodiac_sign(self):
        """Returns """
        if self.date_naissance is None:
            return _('(None)')
        d = self.date_naissance
        return self.ZODIAC_SIGNS[bisect(self.ZODIAC_SIGNS, (d.month, d.day))][2]
    zodiac_sign.short_description = _("Star sign")

    @staticmethod
    def get_or_not_precised(v, lower=False):
        if v:
            return v
        return _('(Not precised)').lower() if lower else _('(Not precised)')

    # Référence de la classe de base User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_beta_tester = models.BooleanField(default=False)
    newsletter_configuration = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_NEWSLETTER_CONFIGURATION.items())],
        default=PersonneEnums.NEWSLETTER_CONFIGURATION_EVERY_WEEK,
        null=True, blank=True)
    newsletter_date_sent = models.DateTimeField(default=None, null=True,
                                                blank=True)

    def est_un_homme(self):
        return self.sexe == PersonneEnums.SEXE_HOMME

    sexe = models.IntegerField(
        choices=[(a, b) for a, b in list(PersonneEnums.TAB_SEXE.items())],
        default=None, null=True, blank=True)
    nb_enfants = models.IntegerField(blank=True, default=0)

    def est_marie(self):
        return self.statut not in [PersonneEnums.STATUT_SOLO]

    custom_zodiac_sign = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_CUSTOM_ZODIAC_SIGN.items())],
        default=None, null=True, blank=True)
    statut = models.IntegerField(
        choices=[(a, b) for a, b in list(PersonneEnums.TAB_STATUT.items())],
        # !! tant que pas premium, forcer à solo :
        default=PersonneEnums.STATUT_SOLO,
        null=True, blank=True)
    est_fumeur = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_EST_FUMEUR.items())],
        default=None, null=True, blank=True)
    est_physique = models.BooleanField(default=True)

    est_active = models.BooleanField(default=True)
    est_detruit = models.DateTimeField(default=None, null=True, blank=True)
    reason_delete = models.TextField(default=None, null=True, blank=True)
    reactivate_code = models.CharField(max_length=200, default=None,
                                       null=True, blank=True)

    one_click_login = models.BooleanField(default=False)

    confirmation_code = models.CharField(max_length=200, default=None,
                                         null=True, blank=True)
    # lorsqu'on invite quelqu'un il a un mot de passe temporaire ici :
    temporary_visible_password = models.CharField(max_length=200, default='',
                                                  blank=True)
    reset_password = models.DateTimeField(default=None, null=True, blank=True)
    champs_supplementaires = models.TextField(default=None, null=True,
                                              blank=True)

    def get_date_naissance(self):
        if self.date_naissance:
            return formats.date_format(self.date_naissance,
                                       "SHORT_DATE_FORMAT")
        return _('(Not precised)')

    def get_age(self):
        if not self.date_naissance:
            return ''
        age = (datetime.date.today() - self.date_naissance).days / 365.25
        return _('{} years old').format(int(age))
    date_naissance = models.DateField(default=None, null=True, blank=True,
                                      verbose_name=_('Birth date'))

    @cached_property
    def photo_profil(self):
        a = PersonnePhoto.objects.filter(
            personne=self, date_v_fin__isnull=True,
            photo_type=PersonnePhoto.PHOTO_PROFIL)
        return a[0] if len(a) else None

    @cached_property
    def photo_banniere(self):
        a = PersonnePhoto.objects.filter(
            personne=self, date_v_fin__isnull=True,
            photo_type=PersonnePhoto.PHOTO_BANNIERE)
        return a[0] if len(a) else None

    @cached_property
    def url_photo_profil(self):
        a = self.photo_profil
        if a:
            return a.photo.url('img/no-user-image.gif')
        else:
            return self.get_url(None, 'img/no-user-image.gif')

    @cached_property
    def url_photo_banniere(self):
        a = self.photo_banniere
        if a:
            return a.photo.url('img/bg/default-background.jpg')
        else:
            return self.get_url(None, 'img/bg/default-background.jpg')

    photos = models.ManyToManyField(Photo, blank=True,
                                    through='PersonnePhoto',
                                    symmetrical=False,
                                    related_name='parent')

    def get_place_of_birth(self, lower=False):
        return self.get_or_not_precised(self.place_of_birth, lower)
    place_of_birth = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE,
                                       default=None, blank=True,
                                       related_name='place_of_birth_tag',
                                       verbose_name=_('Place of birth'))

    def get_place_i_live(self, lower=False):
        return self.get_or_not_precised(self.place_i_live, lower)
    place_i_live = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE,
                                     default=None, blank=True,
                                     related_name='place_i_live_tag',
                                     verbose_name=_('City where I live'))

    @cached_property
    def get_employer_current(self):
        return self.get_or_not_precised(self.employer_current)
    employer_current = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE,
                                         default=None, blank=True,
                                         related_name='employer_current_tag',
                                         verbose_name=_('Current employer'))

    @cached_property
    def get_employer_past(self):
        return self.get_or_not_precised(self.employer_previous)
    employer_previous = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE,
                                          default=None, blank=True,
                                          related_name='employer_previous_tag',
                                          verbose_name=_('Previous employer'))

    """
    (!!) 15 jours de boulot perdus à faire et défaire !!
    """
    # (!) modifications Franck
    langue = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_LANGUE.items())],
        default=None, null=True, blank=True)
    niveau_etudes = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_NIVEAU_ETUDES.items())],
        default=None, null=True, blank=True)
    profession = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_PROFESSION.items())],
        default=None, null=True, blank=True)
    how_did_i_know_cogofly = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_HOW_DID_I_KNOW_COGOFLY.items())],
        default=None, null=True, blank=True)

    """
    Champs à choix multiple
    """
    programmes2 = ManyToManyStillValid(
        TagTraduit, blank=True, default=None, symmetrical=False,
        through='PersonneProgramme',
        related_name='personne_programme')

    activites2 = ManyToManyStillValid(
        TagTraduit, blank=True, default=None, symmetrical=False,
        through='PersonneActivite',
        related_name='personne_activite')

    hobbies2 = ManyToManyStillValid(
        TagTraduit, blank=True, default=None, symmetrical=False,
        through='PersonneHobby',
        related_name='personne_hobby')

    types_permis2 = ManyToManyStillValid(
        TagTraduit, blank=True, default=None, symmetrical=False,
        through='PersonneTypepermis',
        related_name='personne_typepermis')

    personnalites2 = ManyToManyStillValid(
        TagTraduit, blank=True, default=None, symmetrical=False,
        through='PersonnePersonnalite',
        related_name='personne_personnalite')

    langues2 = ManyToManyStillValid(
        TagTraduit, blank=True, default=None, symmetrical=False,
        through='PersonneLangue',
        related_name='personne_langue')

    """
    Visibilité des champs
    """
    niveau_visibilite = models.IntegerField(
        choices=[(a, b) for a, b in
                 list(PersonneEnums.TAB_VISIBILITE.items())],
        default=PersonneEnums.VISIBILITE_TOUT_LE_MONDE, null=True, blank=True)

    def can_see_informations_of(self, other):
        if self == other:
            return True
        if other.niveau_visibilite == PersonneEnums.VISIBILITE_QUE_MOI:
            return False
        if other.niveau_visibilite == PersonneEnums.VISIBILITE_TOUT_LE_MONDE:
            return True
        # arrivé ici = que mes amis qui me voient
        # (!) toutes les relations SAUF "refusee, en cours ou retirée" car
        #     il y a plus de relations "ok" que de relations refusée
        return other.type_of_relation_with(self) not in [
            PersonneEnums.RELATION_INVITATION_REFUSEE,
            PersonneEnums.RELATION_INVITATION_EN_COURS,
            PersonneEnums.RELATION_RETIREE,
            None,  # ! si relation inconnue, alors pas de partage
        ]

    # Tous les booléens :
    age_visible = models.BooleanField(default=True)
    nb_enfants_visible = models.BooleanField(default=True)
    langue_visible = models.BooleanField(default=True)
    langues2_visible = models.BooleanField(default=True)
    niveau_etudes_visible = models.BooleanField(default=True)
    programme_visible = models.BooleanField(default=True)
    employer_current_visible = models.BooleanField(default=True)
    employer_previous_visible = models.BooleanField(default=True)
    profession_visible = models.BooleanField(default=True)
    activite_visible = models.BooleanField(default=True)
    hobbies_visible = models.BooleanField(default=True)
    conduite_visible = models.BooleanField(default=True)
    personnalite_visible = models.BooleanField(default=True)
    est_fumeur_visible = models.BooleanField(default=True)
    custom_zodiac_sign_visible = models.BooleanField(default=True)
    self_description_visible = models.BooleanField(default=True)

    def nb_enfants_description(self):
        if self.nb_enfants:
            return ungettext('{} child', '{} children',
                             self.nb_enfants).format(self.nb_enfants)
        return _('No children')

    def langue_description(self):
        return PersonneEnums.TAB_LANGUE[self.langue] \
            if self.langue is not None else _('not precised')

    def niveau_etudes_description(self):
        return PersonneEnums.TAB_NIVEAU_ETUDES[self.niveau_etudes] \
            if self.niveau_etudes is not None else _('not precised')

    def employer_current_description(self):
        return self.employer_current if self.employer_current \
                                     else _('not precised')

    def employer_previous_description(self):
        return self.employer_previous if self.employer_previous  \
                                      else _('not precised')

    def profession_description(self):
        return PersonneEnums.TAB_PROFESSION[self.profession] \
            if self.profession is not None else _('not precised')

    def est_fumeur_description(self):
        return PersonneEnums.TAB_EST_FUMEUR[self.est_fumeur] \
            if self.est_fumeur is not None else _('not precised')

    def custom_zodiac_sign_description(self):
        print(self.custom_zodiac_sign)
        return PersonneEnums.TAB_CUSTOM_ZODIAC_SIGN[self.custom_zodiac_sign] \
            if self.custom_zodiac_sign is not None else _('not precised')

    def self_description_description(self):
        return self.description if self.description else ''

    # ----------------------------------------------------------------------
    @cached_property
    def description_last_travels(self):

        def desc_voyage(v):
            return v[0].travel.formatted_address \
                if len(v) \
                else _('(not precised)')

        return [_('Latest travel: {}').format(desc_voyage(self.travels_past)),
                _('Next travel : {}').format(desc_voyage(self.travels_futur))]

    @cached_property
    def description_resume(self):
        if self.est_un_homme():
            ne_a = pgettext("Homme", 'Born at {}')
            vit_a = pgettext("Homme", 'Lives at {}')
        else:
            ne_a = pgettext("Femme", 'Born at {}')
            vit_a = pgettext("Femme", 'Lives at {}')
        return [vit_a.format(self.get_place_i_live(lower=True)),
                ne_a.format(self.get_place_of_birth(lower=True))]

    @cached_property
    def contacts(self):
        return self.relations_that_are_not(
            [PersonneEnums.RELATION_INVITATION_EN_COURS,
             PersonneEnums.RELATION_INVITATION_REFUSEE,
             PersonneEnums.RELATION_RETIREE])

    def description_ses_contacts(self):
        if self.est_un_homme():
            sing = pgettext("Homme", 'His contact')
            plur = pgettext("Homme", 'His contacts')
        else:
            sing = pgettext("Femme", 'Her contact')
            plur = pgettext("Femme", 'Her contacts')
        return ungettext(sing, plur, len(self.contacts))

    @cached_property
    def travels_past(self):
        return PersonneTravel.objects.filter(
            Q(date_end__lt=datetime.datetime.now()) |
            (Q(date_start__lt=datetime.datetime.now(), date_end=None)) |
            (Q(date_start=None, date_end=None, is_past=True)),
            personne=self,
            date_v_fin__isnull=True,
        ).order_by('-date_start')

    @cached_property
    def travels_futur(self):
        return PersonneTravel.objects.filter(
            Q(date_end__gte=datetime.datetime.now()) |
            (Q(date_start__gte=datetime.datetime.now(), date_end=None)) |
            (Q(date_start=None, date_end=None, is_past=False)),
            personne=self,
            date_v_fin__isnull=True,
        ).order_by('-date_start')

    # travels = models.ManyToManyField(
    #         TagWithValue, blank=True,
    #         through='PersonneTravel',
    #         default=None, symmetrical=False,
    #         related_name='personne_travel')
    travels = models.ManyToManyField(
            TagGoogleMapsTraduit, blank=True,
            through='PersonneTravel',
            default=None, symmetrical=False,
            related_name='personne_travel')
    self_description = models.TextField(null=True, blank=True,
                                        verbose_name=_('Describe yourself'))

    relations = models.ManyToManyField('self', through='PersonneRelation',
                                       symmetrical=False,
                                       related_name='personne_relations')

    liked = models.ManyToManyField('self', through='PersonneLiked',
                                   symmetrical=False,
                                   related_name='personne_liked')

    def type_of_relation_with(self, other):
        q = Q(src=self) & Q(dst=other)
        # Vérifier si on ne l'a pas déjà en cache car la méthode est appelée
        # plusieurs fois d'affilée, surtout ne pas charger la base de données :
        key = 'rel_{}'.format(str(q))
        retour = self.cache.get(key)
        if retour:
            return retour
        try:
            try:
                r = PersonneRelation.objects.get(q)
            except MultipleObjectsReturned as m:
                r = [a for a in PersonneRelation.objects.filter(q)]
                r = r[-1]
            self.cache[key] = r
            return r
        except ObjectDoesNotExist:
            self.cache[key] = None
            return None

    def type_of_relation_you(self, other):
        # Wrapper pour sortir une phrase du genre "vous êtes invité par"
        r = self.type_of_relation_with(other)
        if not r:
            return None
        r_type = r.type_relation
        if r.is_reverse:
            return PersonneEnums.TAB_RELATIONS_REVERSE_YOU[r_type]\
                .format(other.full_name())
        else:
            return PersonneEnums.TAB_RELATIONS_YOU[r_type]\
                .format(other.full_name())

    def type_of_relation_you_short(self, other):
        # Wrapper pour sortir une phrase courte du genre "vous êtes invité par"
        r = self.type_of_relation_with(other)
        if not r:
            return None
        r_type = r.type_relation
        if r.is_reverse:
            return PersonneEnums.TAB_RELATIONS_REVERSE_YOU_SHORT[r_type]\
                .format(other.full_name())
        else:
            return PersonneEnums.TAB_RELATIONS_YOU_SHORT[r_type]\
                .format(other.full_name())

    def can_remove_relation(self, other):
        r = self.type_of_relation_with(other)
        if not r:
            return False
        return r.type_relation not in [
            PersonneEnums.RELATION_INVITATION_REFUSEE,
            PersonneEnums.RELATION_INVITATION_EN_COURS,
            PersonneEnums.RELATION_RETIREE]

    def relations_of_type(self, type_relation):
        # Qui aurait cru qu'aller chercher les amis était une tâche aussi
        # lourde ? Chercher les relations qui :
        # - sont de type ami et user = src ou user = dst
        # À partir de là on a les id -> ressortir les personnes avec ces ids.
        # chain = convertir les querysets en tableau
        # http://stackoverflow.com/questions/
        # 6732298/join-multiple-querysets-from-different-base-models-django
        id_personnes = list(chain(
            PersonneRelation.objects.filter(
                Q(type_relation__exact=type_relation) & Q(src=self)
            ).values_list('dst', flat=True),
            PersonneRelation.objects.filter(
                Q(type_relation__exact=type_relation) & Q(dst=self)
            ).values_list('src', flat=True)))
        return Personne.objects.filter(pk__in=id_personnes,
                                       date_v_fin__isnull=True)

    def relations_that_are_not(self, types_relations):
        # cf méga commentaire sur relations_of_type()
        n = Q()
        for r in types_relations:
            n = n & (~Q(type_relation__exact=r))
        id_personnes = list(chain(
            PersonneRelation.objects.filter(
                n & Q(src=self)
            ).values_list('dst', flat=True),
            PersonneRelation.objects.filter(
                n & Q(src=self)
            ).values_list('src', flat=True)))
        return Personne.objects\
            .filter(pk__in=id_personnes)\
            .exclude(pk__exact=self.pk)

    def profile_complete(self):
        return all([self.get_nom(), self.get_prenom(),
                    self.sexe is not None, self.date_naissance is not None,
                    self.place_i_live])

    def get_infos_name(self, tab):
        # Essai de récupérer ce qu'on demande, sinon on renvoie quelque chose :
        def g(x):
            return x if x else ''
        retour = ' '.join([g(a) for a in tab]).strip()
        if not retour:
            retour = g(self.user.username)
            p = retour.find('_at_')
            retour = retour[:p-1 if p > 0 else None]
        if not retour:
            retour = g(self.user.email).strip()
            p = retour.find('@')
            retour = retour[:p-1 if p > 0 else None]
        return retour

    def get_prenom(self):
        return self.get_infos_name([self.user.first_name])

    def get_nom(self):
        return self.get_infos_name([self.user.last_name])

    def full_name(self):
        return self.get_infos_name([self.user.first_name, self.user.last_name])

    def __str__(self):
        return _('Person : {} / {} {}').format(
            self.user.email, self.user.first_name, self.user.last_name
        ).strip()

    class Meta(BaseModel.Meta):
        ordering = ['date_v_debut']


@python_2_unicode_compatible
class PersonneSearch(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    search = models.ForeignKey(TagGoogleMapsTraduit, on_delete=models.CASCADE,  verbose_name=_('Search'))

    def __str__(self):
        d = self.date_last_modif
        return '{}/{:0>2}/{:0>2} - {:0>2}:{:0>2}:{:0>2} : {} / {}'.format(
            d.year, d.month, d.day, d.hour, d.minute, d.second,
            self.personne.full_name(), self.search.formatted_address)

    class Meta(BaseModel.Meta):
        ordering = ['date_v_debut']
        verbose_name = _('Person / search')
        verbose_name_plural = _('Person / searches')


@python_2_unicode_compatible
class PersonneProgramme(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    programme = models.ForeignKey(TagTraduit, on_delete=models.CASCADE,  verbose_name=_('Subject'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.programme)


@python_2_unicode_compatible
class PersonneActivite(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    activite = models.ForeignKey(TagTraduit, on_delete=models.CASCADE,  verbose_name=_('Activity sector'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.activite)


@python_2_unicode_compatible
class PersonneHobby(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    hobby = models.ForeignKey(TagTraduit, on_delete=models.CASCADE,  verbose_name=_('Hobby'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.hobby)


@python_2_unicode_compatible
class PersonneTypepermis(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    type_permis = models.ForeignKey(TagTraduit, on_delete=models.CASCADE,  verbose_name=_('Licence'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.type_permis)


@python_2_unicode_compatible
class PersonnePersonnalite(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    personnalite = models.ForeignKey(TagTraduit, on_delete=models.CASCADE,  verbose_name=_('Personality'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.personnalite)


@python_2_unicode_compatible
class PersonneLangue(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    langue = models.ForeignKey(TagTraduit, on_delete=models.CASCADE,  verbose_name=_('Language'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.langue)


@python_2_unicode_compatible
class PersonneTravel(BaseModel):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    travel = models.ForeignKey(TagGoogleMapsTraduit, on_delete=models.CASCADE,  verbose_name=_('Travel'))
    comments = models.TextField(null=True, blank=True,
                                verbose_name=_('Comments'))

    def urls_photos(self):
        return [x for x in list({self.photo1.url() if self.photo1 else None,
                                 self.photo2.url() if self.photo2 else None,
                                 self.photo3.url() if self.photo3 else None})
                if x is not None]

    photo1 = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='photo1',
                               verbose_name=_('Travel picture 1'))
    photo2 = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='photo2',
                               verbose_name=_('Travel picture 2'))
    photo3 = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='photo3',
                               verbose_name=_('Travel picture 3'))

    date_start = DatePartialField(
        default=None, null=True, blank=True, editable=True,
        verbose_name=_("Start ({})").format(
            get_format('DATE_INPUT_FORMATS')[1]).replace('%', ''))
    date_end = DatePartialField(
        default=None, null=True, blank=True, editable=True,
        verbose_name=_("End ({})").format(
            get_format('DATE_INPUT_FORMATS')[1]).replace('%', ''))

    # utile que si date_start et date_start null :
    is_past = models.BooleanField(default=False, blank=True,
                                  verbose_name=_('This is a past travel'))

    def description_dates(self):
        d_s = self.date_start
        d_e = self.date_end
        d_s = d_s.canonical_version if d_s else ''
        d_e = d_e.canonical_version if d_e else ''
        if d_s and d_e:
            return _('From {} until {}').format(d_s, d_e)
        elif d_s:
            return _('From {} until (not precised)').format(d_s)
        elif d_e:
            return _('From (not precised) until {}').format(d_e)
        else:
            return _('No date precised').format(d_s)

    def comments_summary(self):
        a = self.comments
        if a:
            return (a[:85] + '&raquo;...') if len(a) > 90 else a
        return ''

    def description(self):
        a = self.travel.formatted_address
        dd = self.description_dates()
        if self.comments:
            s = MLStripper()
            s.feed(self.comments)
            c = s.get_data().replace('\n', ' ').replace('\r', '')
            c = (c[:85] + '...') if len(c) > 90 else c
        else:
            c = ''

        return '{}{}{}'.format(a, ' ({})'.format(dd.lower()) if dd else '',
                                ' ({})'.format(c) if c else '').strip()

    def description_complete(self, strip=100):
        if self.date_start is None and self.date_end is None:
            past = self.is_past
        elif self.date_start is None:  # que date fin existante
            past = self.date_end < datetime.datetime.now()
        else:
            past = self.date_start < datetime.datetime.now()
        c = '{} {} {}'.format(
            self.personne.full_name(),
            _('went to') if past else _('would like to go to'),
            self.description()
        )
        if strip and len(c) > strip:
            c = (c[:strip] + '...')
        return c

    def __str__(self):
        return _('{} / {}').format(self.personne, self.travel)


@python_2_unicode_compatible
class PersonnePhoto(PictureURL, BaseModel):
    PHOTO_PROFIL = 0
    PHOTO_VOYAGE = 1
    PHOTO_BANNIERE = 2
    PHOTO_POUR_BLOG = 3
    PHOTO_POUR_PUB = 4
    TAB_PHOTO = {
        PHOTO_PROFIL: _('Profil'),
        PHOTO_VOYAGE: _('Travel'),
        PHOTO_BANNIERE: _('Banner'),
        PHOTO_POUR_BLOG: _('Blog'),
        PHOTO_POUR_PUB: _('Advert'),
    }

    photo_type = models.IntegerField(
        choices=[(a, b) for a, b in list(TAB_PHOTO.items())],
        default=PHOTO_PROFIL)
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE,  verbose_name=_('Person'))
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,  verbose_name=_('Picture'))

    def __str__(self):
        return _('{} / {}').format(self.personne, self.photo)

    class Meta(BaseModel.Meta):
        ordering = ['date_v_debut']
        verbose_name = _('Person / photo')
        verbose_name_plural = _('Person / photos')


@python_2_unicode_compatible
class ActiviteShared(BaseModel):
    src = models.ForeignKey(Personne, default=None, blank=True, on_delete=models.CASCADE,
                            related_name='shared_by',
                            null=True, verbose_name=_('Shared by'))

    dst = models.ForeignKey(Personne, default=None, blank=True, on_delete=models.CASCADE,
                            related_name='shared_to',
                            null=True, verbose_name=_('Shared to'))
    activite = models.ForeignKey('Activite', default=None, blank=True, on_delete=models.CASCADE,
                                 null=True, verbose_name=_('Activity sector'))

    def __str__(self):
        d = self.date_last_modif
        return '{}/{:0>2}/{:0>2} - {:0>2}:{:0>2}:{:0>2} : ' \
               '{} -> {} / {}'.format(
                   d.year, d.month, d.day, d.hour, d.minute, d.second,
                   self.src.full_name(), self.dst.full_name(),
                   self.activite.description() if self.activite else '??')

    class Meta(BaseModel.Meta):
        ordering = ['-date_last_modif']


@python_2_unicode_compatible
class Activite(BaseModel):
    ACTIVITE_AJOUT_RELATION = 0
    ACTIVITE_AJOUT_VOYAGE = 1
    ACTIVITE_MODIFIE_VOYAGE = 2
    ACTIVITE_BLOG = 3
    ACTIVITE_COMMENT = 4
    ACTIVITE_TESTIMONY = 5
    ACTIVITE_EXPRESSYOURSELF = 6
    TAB_ACTIVITES = {
        ACTIVITE_AJOUT_RELATION: _('has a new relationship:'),
        ACTIVITE_AJOUT_VOYAGE: _('has a new travel:'),
        ACTIVITE_MODIFIE_VOYAGE: _("has changed a travel, it's now:"),
        ACTIVITE_BLOG: _("Cogofly's news"),
        ACTIVITE_COMMENT: _("has made a comment:"),
        ACTIVITE_TESTIMONY: _("has made a testimony:"),
        ACTIVITE_EXPRESSYOURSELF: _("has expressed this:"),
    }
    activite = models.IntegerField(
        choices=[(a, b) for a, b in list(TAB_ACTIVITES.items())],
        default=ACTIVITE_AJOUT_RELATION)

    travel = models.ForeignKey(PersonneTravel, default=None, blank=True, on_delete=models.CASCADE,
                               null=True, verbose_name=_('Travel'))
    relation = models.ForeignKey('PersonneRelation', default=None, blank=True, on_delete=models.CASCADE,
                                 null=True, verbose_name=_('Relationship'))
    blog_traduit = models.ForeignKey(BlogTraduit, default=None, blank=True, on_delete=models.CASCADE,
                                     null=True,
                                     help_text=_('Blog translated'),
                                     verbose_name=_('Blog translated'))
    comment = models.ForeignKey('ActiviteComments', null=True, on_delete=models.CASCADE,
                                default=None, blank=True,
                                related_name='activite',)
    express_yourself = models.ForeignKey('ActiviteExpressyourself', null=True, on_delete=models.CASCADE,
                                         default=None, blank=True,
                                         related_name='activite',)
    testimony = models.ForeignKey('ActiviteTestimony', null=True, on_delete=models.CASCADE,
                                  default=None, blank=True,
                                  related_name='activite',)
    date_publication = models.DateTimeField(default=timezone.now,
                                            verbose_name=_('Created'))

    @staticmethod
    def persons_description(tab):
        if not len(tab):
            return None
        if len(tab) == 1:
            return tab[0].full_name()
        a = [p.full_name() for p in tab]
        return _('{} and {}').format(', '.join(a[:-1]), a[-1])

    def persons_who_shared_this_to(self, person):
        # traduction de ce qui suit :
        # return personnes dont pk = dans les activités partagées *À* "person"
        s = set(ActiviteShared.objects.filter(activite=self, dst=person)
                .values_list('src', flat=True))
        return self.persons_description(Personne.objects.filter(pk__in=s))

    def person_who_shared_this_is(self, person):
        # traduction de ce qui suit :
        # return personnes dont pk = dans les activités partagées *PAR* "person"
        s = set(ActiviteShared.objects.filter(activite=self, src=person)
                .values_list('dst', flat=True))
        return self.persons_description(Personne.objects.filter(pk__in=s))

    def description_resume(self):
        return self.description(max_len=80)

    def description(self, max_len=None, with_date=True, tag=None,
                    website='', with_link=False):
        def wrap_with_link(s):
            if not with_link:
                return s.full_name()
            return '<a href="{}{}">{}</a>'.format(
                website, reverse_lazy('contact_detail', args=(s.id,)),
                s.full_name())

        if self.date_last_modif and with_date:
            d = '{}, {} : '.format(
                date_format(self.date_last_modif, 'DATE_FORMAT'),
                date_format(self.date_last_modif, 'TIME_FORMAT'))
        else:
            d = ''

        a = self.TAB_ACTIVITES[self.activite]
        try:
            if self.activite == self.ACTIVITE_BLOG:
                x = str(self.blog_traduit)
                y = ''
            elif self.activite == self.ACTIVITE_AJOUT_RELATION:
                x = wrap_with_link(self.relation.src)
                y = wrap_with_link(self.relation.dst)
            elif self.activite == self.ACTIVITE_COMMENT:
                x = wrap_with_link(self.comment.personne)
                y = self.comment.activite_dst.description()
            elif self.activite == self.ACTIVITE_TESTIMONY:
                x = wrap_with_link(self.testimony.personne)
                y = self.testimony.testimony if self.testimony.testimony else ''
            elif self.activite == self.ACTIVITE_EXPRESSYOURSELF:
                x = wrap_with_link(self.express_yourself.personne)
                y = self.express_yourself.message \
                    if self.express_yourself.message else ''
            else:
                x = wrap_with_link(self.travel.personne)
                y = str(self.travel.description())
        except ObjectDoesNotExist:
            x = y = '***'
        except AttributeError as e:
            x = y = '??? ({})'.format(str(e))
        if tag is None:
            retour = '{}{}'.format(d, ' '.join([x, str(a), y])).strip()
        else:
            retour = '{}{}'.format(d, ' '.join([
                '<{}>{}</{}>'.format(tag, x, tag),
                str(a),
                '<{}>{}</{}>'.format(tag, y, tag),
            ])).strip()
        # if self.shared_src and self.shared_dst:
        #     retour = _(u'{} shared this: {}').format(
        #         self.shared_src.full_name(), retour)
        return retour

    def description_with_link(self, max_len=None, with_date=True, tag=None):
        return self.description(max_len=max_len, with_date=with_date,
                                tag=tag, with_link=True)

    def __str__(self):
        d = self.date_publication
        if self.blog_traduit:
            retour = str(self.blog_traduit)
        else:
            retour = self.description()
        retour = '{}/{:0>2}/{:0>2} - {:0>2}:{:0>2}:{:0>2} : {}'.format(
            d.year, d.month, d.day, d.hour, d.minute, d.second, retour)
        # if self.shared_src:
        #     retour = u'{} (shared: {} -> {})'.format(
        #         retour, self.shared_src.full_name(),
        #         self.shared_dst.full_name())
        return retour

    class Meta(BaseModel.Meta):
        ordering = ['-date_publication', '-date_last_modif']


@python_2_unicode_compatible
class PersonneActiviteNewsletter(BaseModel):
    personne = models.ForeignKey(Personne, default=None, blank=True, on_delete=models.CASCADE,
                                 null=True, verbose_name=_('To'), )
    activite = models.ForeignKey(Activite, default=None, blank=True, on_delete=models.CASCADE,
                                 null=True, verbose_name=_('Activity'), )
    date_sent = models.DateTimeField(default=None, null=True, blank=True,
                                     verbose_name=_('Sent'), )

    def __str__(self):
        return '{} : {} - {}'.format(self.to_str(self.personne),
                                      self.to_str(self.activite),
                                      self.to_str(self.date_sent))

    class Meta(BaseModel.Meta):
        ordering = ['-date_last_modif', '-date_v_debut']


@python_2_unicode_compatible
class PersonneBlogNewsletter(BaseModel):
    personne = models.ForeignKey(Personne, default=None, blank=True, on_delete=models.CASCADE,
                                 null=True, verbose_name=_('To'), )
    blog = models.ForeignKey(Blog, default=None, blank=True, on_delete=models.CASCADE,
                             null=True, verbose_name=_('Blog'), )
    date_sent = models.DateTimeField(default=None, null=True, blank=True,
                                     verbose_name=_('Sent'), )

    def __str__(self):
        return '{} : {} - {}'.format(self.to_str(self.personne),
                                      self.to_str(self.blog),
                                      self.to_str(self.date_sent))

    class Meta(BaseModel.Meta):
        ordering = ['-date_last_modif', '-date_v_debut']


@python_2_unicode_compatible
class ActiviteComments(BaseModel):
    personne = models.ForeignKey('Personne', null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='personne_comment')
    # L'activité commentée :
    activite_dst = models.ForeignKey('Activite', null=True, blank=True, on_delete=models.CASCADE,  )
    comment = models.TextField(null=True, blank=True,
                               verbose_name=_('Comment'))

    def description(self, with_link=True):
        def wrap_with_link(s):
            if not with_link:
                return s.full_name()
            return '<a href="{}" target="_blank">{}</a>'.format(
                reverse_lazy('contact_detail', args=(s.id,)),
                s.full_name())

        if self.date_last_modif:
            d = '{}, {}: '.format(
                date_format(self.date_last_modif, 'DATE_FORMAT'),
                date_format(self.date_last_modif, 'TIME_FORMAT'))
        else:
            d = ''
        return _('{}{} has commented: {}{}').format(
            d, wrap_with_link(self.personne),
            self.comment[:80] if self.comment else '',
            '...' if len(self.comment) > 80 else '')

    def __str__(self):
        return '{} --> {} ({}{})'.format(
            str(self.personne.full_name()),
            str(self.activite_dst.description()),
            self.comment[:80] if self.comment else '',
            '...' if len(self.comment) > 80 else '')

    class Meta:
        ordering = ['-date_last_modif']
        verbose_name = _("Activity / comment")
        verbose_name_plural = _("Activities / comments")


@python_2_unicode_compatible
class ActiviteExpressyourself(BaseModel):
    personne = models.ForeignKey('Personne', null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='personne_expressyourself')
    message = models.TextField(null=True, blank=True,
                               verbose_name=_('Message'))

    def __str__(self):
        return '{} --> {} ({}{})'.format(
            str(self.personne.full_name()),
            str(self.message),
            self.message[:80] if self.message else '',
            '...' if len(self.message) > 80 else '')

    class Meta:
        ordering = ['-date_last_modif']
        verbose_name = _("Activity / express yourself")
        verbose_name_plural = _("Activities / express yourself")


@python_2_unicode_compatible
class ActiviteTestimony(BaseModel):
    personne = models.ForeignKey('Personne', null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='personne_testimony')
    # Témoignage :
    testimony = models.TextField(null=True, blank=True,
                                 verbose_name=_('Testimony'))
    testimony_show_name = models.BooleanField(
        default=False,
        verbose_name=_('Show name and picture'),
        help_text=_('Shows the name and '
                    'profile picture inside the testimony page'))
    validated_by_moderator = models.BooleanField(default=False)

    def description(self):
        if self.date_last_modif:
            d = '{}, {}: '.format(
                date_format(self.date_last_modif, 'DATE_FORMAT'),
                date_format(self.date_last_modif, 'TIME_FORMAT'))
        else:
            d = ''
        return _('{}{} testified into the site: {}{}').format(
            d, str(self.personne.full_name()),
            self.testimony[:80] if self.testimony else '',
            '...' if len(self.testimony) > 80 else '')

    def __str__(self):
        return self.description()

    class Meta:
        ordering = ['-date_last_modif']
        verbose_name = _("Activity / testimony")
        verbose_name_plural = _("Activities / testimonies")


@python_2_unicode_compatible
class PersonneRelation(BaseModel):

    type_relation = models.IntegerField(
        choices=[(a, b) for a, b in list(PersonneEnums.TAB_RELATIONS.items())],
        default=PersonneEnums.RELATION_AMI)
    src = models.ForeignKey('Personne', on_delete=models.CASCADE,  related_name='relation_src')
    dst = models.ForeignKey('Personne', on_delete=models.CASCADE,  related_name='relation_dst')
    opposite = models.ForeignKey('PersonneRelation', on_delete=models.CASCADE,
                                 null=True, blank=True, default=None)
    is_reverse = models.BooleanField(default=False)
    raison_refus = models.IntegerField(
        choices=[(a, b) for a, b in list(PersonneEnums.TAB_INVITATION.items())],
        default=PersonneEnums.INVITATION_REFUS_NON_MERCI,
        null=True, blank=True)

    def description(self, tag_around=None):
        return _('The {}, {}{}{} has invited you.').format(
            str(self.date_creation_relative()),
            '<{}>'.format(tag_around) if tag_around else '',
            str(self.src.full_name()),
            '</{}>'.format(tag_around) if tag_around else '',)

    def __str__(self):
        return _('n.{} {} : {} : {}').format(
                str(self.pk), str(self.src.full_name()),
                PersonneEnums.TAB_RELATIONS[self.type_relation]
                if not self.is_reverse
                else PersonneEnums.TAB_RELATIONS_REVERSE[self.type_relation],
                str(self.dst.full_name()))

    def save(self, *args, **kwargs):
        retour = super(PersonneRelation, self).save(args, kwargs)
        return retour

    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')


@python_2_unicode_compatible
class PersonneLiked(BaseModel):

    src = models.ForeignKey('Personne', on_delete=models.CASCADE,  related_name='liked_src')
    dst = models.ForeignKey('Personne', on_delete=models.CASCADE,  related_name='liked_dst')
    activite = models.ForeignKey('Activite', related_name='liked_activite', on_delete=models.CASCADE,
                                 null=True, blank=True, default=None)
    # liked = si on a ajouté ou enlevé le pouce :
    liked = models.BooleanField(default=True)
    viewed = models.BooleanField(default=False)

    def description(self, tag_around=None):
        return '{}, {}{}{} {} {}'.format(
            str(self.date_creation_relative()),
            '<{}>'.format(tag_around) if tag_around else '',
            self.src.full_name(),
            '</{}>'.format(tag_around) if tag_around else '',
            pgettext("a aimé", 'liked') if self.liked
            else pgettext("n'a plus aimé", 'disliked'),
            _('your profile') if self.activite is None
            else '"{}"'.format(self.activite.description())
        )

    def __str__(self):
        return _('n.{} : {} --> {} : {}').format(
            self.pk,
            self.src.full_name(),
            self.dst.full_name(),
            _('liked') if self.liked else _('disliked'))

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


@receiver(post_save, sender=PersonneRelation)
def signal_receiver_personne_relation(sender, **kwargs):
    """
    Seule manière de pouvoir créer une relation "opposée" : après l'insert
    en base, faire un autre insert :
    """
    created = kwargs['created']
    obj = kwargs['instance']
    if created:
        if not obj.opposite:
            opposite = PersonneRelation(
                src=obj.dst, dst=obj.src, opposite=obj,
                type_relation=obj.type_relation, is_reverse=True)
            opposite.save()
            obj.opposite = opposite
            obj.save()
    elif not created and obj.type_relation != obj.opposite.type_relation:
        obj.opposite.type_relation = obj.type_relation
        obj.opposite.save()


@receiver(post_save, sender=PersonneTravel)
def signal_receiver_personne_travel(sender, **kwargs):
    """
    Lorsqu'on crée un nouveau voyage, créer l'activité qui va avec :
    """
    created = kwargs['created']
    obj = kwargs['instance']
    if created:
        activite = Activite.ACTIVITE_AJOUT_VOYAGE
    else:
        activite = Activite.ACTIVITE_MODIFIE_VOYAGE
    Activite.objects.create(activite=activite, travel=obj)


@receiver(post_save, sender=BlogTraduit)
def signal_receiver_blog_traduit(sender, **kwargs):
    """
    Lorsqu'on modifie un blog traduit = blog_traduit, mettre à jour
    toutes les activités où il est :
    """
    obj = kwargs['instance']
    activites = Activite.objects.filter(blog_traduit=obj)
    if len(activites):
        # Mettre à jour les dates de publication :
        activites.update(date_publication=obj.blog.date_publication)
    else:
        Activite.objects.create(activite=Activite.ACTIVITE_BLOG,
                                blog_traduit=obj,
                                date_publication=obj.blog.date_publication)


@receiver(post_save, sender=Blog)
def signal_receiver_blog(sender, **kwargs):
    """
    Lorsqu'on modifie un blog -> mettre à jour tous les blog_traduits
    des activités où ils sont :
    """
    obj = kwargs['instance']
    blog_traduits = obj.blogtraduit_set.values_list('pk', flat=True)
    activites = Activite.objects.filter(blog_traduit__in=blog_traduits)
    # Mettre à jour les dates de publication :
    activites.update(date_publication=obj.date_publication)

# vinaigrette.register(Langue, ['nom'])

