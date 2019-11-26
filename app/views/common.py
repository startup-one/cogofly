# coding=UTF-8


import math
# Documentation ici :
# https://docs.djangoproject.com/fr/1.8/topics/class-based-views/intro/
# Ajouter #s-mixins-that-wrap-as-view
import codecs

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy, resolve
from django.db.models import Q, Max
from django.utils import translation
from django.utils.formats import get_format
from django.utils.timezone import make_aware
from django.utils.translation import ugettext as _

from app.models.conversation import Conversation
from app.models.generic import Langue
from app.models.personne import Personne, PersonneRelation, PersonneLiked, \
    ActiviteShared, Activite
from app.models.personne_enums import PersonneEnums
from app.models.publicite import PubliciteTraduit
from app.views.common_mixins import MessagesNotReadMixin, InvitationsMixin, \
    LikesMixin


class LogTemporaire(object):

    @staticmethod
    def write_log(message):
        f = codecs.open('./log', 'a+', "utf-8")
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        f.write(' {}\n'.format(message))
        f.close()


class HQFPaginator(Paginator):
    """
    Classe qui a un paginateur "custom" : on définit les "boundaries" = bornes
    et à partir de là on appelle set_around() qui construit le tableau "around"
    Ce tableau crée un set qui est compris entre les "bornes -/+" du début.
    Cela permet d'avoir :
    - un lien vers début
    - des liens vers précédent/suivant (nb max liens = bornes)
    - un lien vers la fin
    """
    def __init__(self, object_list, per_page, boundaries=3, orphans=0,
                 allow_empty_first_page=True):
        self.boundaries = boundaries
        self.around = []
        super(HQFPaginator, self).__init__(object_list, per_page, orphans,
                                           allow_empty_first_page)

    def get_around(self):
        return self.around

    def set_boundaries(self, boundaries):
        self.boundaries = boundaries

    def set_around(self, number, first=True, last=True):
        retour = []
        if first:
            retour.append({'page': 1, 'first': True,
                           'is_current': 1 == number})
        if (number >= 1) and (number <= self.num_pages):
            i = max(2 if first else 1, number - self.boundaries)
            while i <= (number + self.boundaries) and (i < self.num_pages):
                retour.append({'page': i,
                               'is_current': i == number, })
                i += 1

        if last:
            retour.append({'page': self.num_pages,
                           'is_current': self.num_pages == number,
                           'last': True, })

        self.around = retour
        return retour


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)

        # (!!) multilangue = reverse_lazy, PAS reverse
        return login_required(view, login_url=reverse_lazy('my_home_login'))


class CommonView(MessagesNotReadMixin, InvitationsMixin, LikesMixin):

    def __init__(self, view, *args, **kwargs):
        # Récupérer les infos pour afficher "Bonjour, Mr xx"
        if view.request.user.is_authenticated:
            try:
                p = Personne.objects.get(user=view.request.user)
            except Personne.DoesNotExist:
                p = None
        else:
            p = None

        # ------------------------------------------------
        # (!!!) OPTIMISATION A FAIRE : pour chaque page, cette requête
        #       est faite !! --> Dès qu'il y aura plusieurs milliers de
        #       messages le serveur ne tiendra plus. Optimisation à imaginer :
        #       mettre ces compteurs dans le modèle "personne", et les
        #       modifier lorsqu'il y a un événement correspondant
        #       (message, invitation ou like) puis mettre uniquement ces
        #       compteurs ici :
        if p:
            messages_not_read_count = self.messages_not_read(p).count()

            invitations = self.invitations(p)
            invitations_count = invitations.count()

            likes = self.likes(p)
            likes_count = likes.count()
        else:
            messages_not_read_count = 0
            invitations = None
            invitations_count = 0
            likes = None
            likes_count = 0
        # ------------------------------------------------

        self.infos = {
            'personne': p,
            'hello': _('Hello, {}').format(p.get_prenom() if p else ''),
            'langues_actives':  # order by pour avoir l'anglais en premier
            Langue.objects.filter(active=True).order_by('nom_local'),
            'locale': kwargs.get('langue', None),
            'current_url': resolve(view.request.path_info).url_name,
            'slug': view.kwargs.get('slug', None),
            'date_format': get_format('DATE_FORMAT'),
            'short_date_format': get_format('SHORT_DATE_FORMAT'),
            'translated_urls': [],

            'notifications': {
                'total': messages_not_read_count + invitations_count +
                likes_count,
                'messages_not_read_count': messages_not_read_count,
                'invitations': invitations,
                'invitations_count': invitations_count,
                'likes': likes,
                'likes_count': likes_count
            }
        }
        if self.infos['locale']:
            translation.activate(self.infos['locale'])
        else:
            self.infos['locale'] = translation.get_language()

        # (!) Refaire passer le paramètre de l'URL qu'on a récupéré.
        #     Actuellement tous mes paramètres des URLs sur lesquelles
        #     je veux faire un reverse_lazy() sont nommés "slug", donc je
        #     le code en dur, puis j'y merge les autres paramètres :
        if self.infos['slug']:
            k = {'slug': self.infos['slug']}
        else:
            k = {}
        k.update(kwargs)

        for l in self.infos['langues_actives']:
            save = translation.get_language()
            translation.activate(l.locale)
            self.infos['translated_urls'].append({
                'nom_local': l.nom_local,
                'locale': l.locale,
                'url_drapeau': l.url_drapeau,
                'slug': str(reverse_lazy(self.infos['current_url'], kwargs=k))
            })
            translation.activate(save)

