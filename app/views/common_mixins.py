# coding=UTF-8
# fichier qui contient les mixins utilisés par les views ET les batches


import math

from datetime import datetime
from django.db.models import Q, Max
from django.utils import translation
from django.utils.timezone import make_aware
from django.utils.translation import ugettext as _

from app.models.conversation import Conversation
from app.models.personne import PersonneRelation, PersonneLiked, \
    ActiviteShared, Activite, PersonneTravel
from app.models.personne_enums import PersonneEnums
from app.models.publicite import PubliciteTraduit


class ProgressionMixin:

    def __init__(self):
        pass

    @staticmethod
    def progression(user, personne):
        retour = {'percent': 0.0, 'missing': []}

        def local_add(v, missing, percent):
            if v:
                retour['percent'] += percent
            else:
                retour['missing'].append(missing)

        local_add(user.first_name, _("first name"), 5.0)
        local_add(user.last_name, _("last name"), 5.0)
        local_add(user.email, _("email"), 5.0)
        local_add(personne.sexe is not None, _("gender"), 5.0)
        local_add(personne.place_i_live, _("where you live"), 5.0)
        local_add(personne.date_naissance, _("when you were born"), 5.0)

        nb = PersonneTravel.objects.filter(personne=personne,
                                           date_v_fin__isnull=True).count()
        local_add(nb, _("at least one travel"), 20.0)

        local_add(personne.place_of_birth, _("where you were born"), 2.14)
        local_add(personne.langue, _("mother tongue"), 2.14)

        local_add(personne.url_photo_profil, _("a profile picture"), 6.67)
        local_add(personne.url_photo_banniere, _("a banner picture"), 5.00)
        local_add(personne.nb_enfants is not None,
                  _("how many children you have"), 1.43)

        local_add(personne.langues2.count(), _("other spoken languages"), 6.67)
        local_add(personne.niveau_etudes, _("level of study"), 2.14)
        local_add(personne.programmes2.count(), _("subjects"), 1.43)
        local_add(personne.employer_current, _("current employer"), 2.14)
        local_add(personne.employer_previous, _("previous employer"), 1.43)
        local_add(personne.profession, _("job"), 2.14)
        local_add(personne.activites2.count(), _("activities"), 1.43)
        local_add(personne.hobbies2.count(), _("hobbies"), 2.14)
        local_add(personne.types_permis2.count(), _("driving licences"), 1.43)
        local_add(personne.personnalites2.count(), _("personality"), 2.14)
        local_add(personne.est_fumeur is not None,
                  _("whether you smoke"), 1.43)
        local_add(personne.custom_zodiac_sign, _("star sign"), 1.43)
        local_add(personne.self_description, _("a description of you"), 6.67)

        if len(retour['missing']) == 0:
            retour['percent'] = 100
        else:
            retour['percent'] = int(math.ceil(retour['percent']))
        return retour


class PubliciteMixin:

    def __init__(self):
        pass

    @staticmethod
    def publicites(publicite_position):
        d = make_aware(datetime.now())
        return PubliciteTraduit.objects.filter(
            Q(publicite__position__exact=publicite_position,
              locale__exact=translation.get_language(),
              date_v_debut__lte=d,) &
            (Q(date_v_fin__isnull=True) | Q(date_v_fin__lte=d))
        ).order_by('publicite__ordre_si_top')


class ActivitesMixin:

    def __init__(self):
        pass

    @staticmethod
    def activites(personne, locale):
        amis = [a.dst.pk for a in PersonneRelation.objects.filter(
            src=personne, type_relation=PersonneEnums.RELATION_AMI)]
        shares = ActiviteShared.objects.filter(dst=personne,
                                               date_v_fin__isnull=True)
        shares = set(shares.values_list('activite__pk', flat=True))
        return Activite.objects.filter(
            # express yourself:
            Q(activite__exact=Activite.ACTIVITE_EXPRESSYOURSELF) |
            # toutes les activités partagées par les autres :
            Q(pk__in=shares) |
            # si un ami a fait un témoignage validé par un modérateur :
            Q(activite__exact=Activite.ACTIVITE_TESTIMONY,
              testimony__personne__pk__in=amis,
              testimony__validated_by_moderator__exact=True) |
            # toutes les activités des voyages de ses amis :
            Q(travel__personne__pk__in=amis) | Q(relation__src__pk__in=amis) |
            # tous les "blogs" de la langue en cours :
            Q(activite__exact=Activite.ACTIVITE_BLOG,
              blog_traduit__locale=locale),
        ).annotate(mx=Max('activiteshared__date_last_modif')).order_by(
            '-blog_traduit__blog__ordre_si_top',
            # ! order by shared date *before anything else* to have shared
            #   event EVEN THOUGH THEY'RE VERY OLD:
            '-date_publication',
            '-date_last_modif',
            '-mx',)


class MessagesNotReadMixin:

    def __init__(self):
        pass

    @staticmethod
    def messages_not_read(personne):
        return Conversation.objects.filter(
            Q(messages__src__est_active=True) &
            Q(messages__dst=personne, messages__is_read=False) &
            Q(date_v_fin__isnull=True))


class MessagesNotReadAndNotNotifiedByMailMixin:

    def __init__(self):
        pass

    @staticmethod
    def messages_not_read_and_not_notified_by_mail(personne):
        return Conversation.objects.filter(
            Q(messages__src__est_active=True) &
            Q(messages__dst=personne, messages__is_read=False) &
            Q(messages__dst_message_unread_notified__isnull=True) &
            Q(date_v_fin__isnull=True))


class InvitationsMixin:

    def __init__(self):
        pass

    @staticmethod
    def invitations(personne):
        return PersonneRelation.objects.filter(
            Q(src__est_active=True) &
            Q(dst=personne) & Q(is_reverse=False) &
            Q(type_relation=PersonneEnums.RELATION_INVITATION_EN_COURS) &
            Q(date_v_fin__isnull=True)
        ).order_by('-date_v_debut')


class LikesMixin:

    def __init__(self):
        pass

    @staticmethod
    def likes(personne):
        return PersonneLiked.objects.filter(
            Q(src__est_active=True) & Q(dst=personne) & Q(viewed=False) &
            Q(date_v_fin__isnull=True))


