# coding=UTF-8



from django.core.exceptions import ValidationError
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import Q, Count
from django.utils import translation
from django.utils.html import MLStripper
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.search.advanced import SearchAdvancedForm
from app.forms.search.basic import SearchBasicForm
from app.models.date_partial_field import parse_date_partial
from app.models.personne_enums import PersonneEnums
from app.models.tag import BaseTag, TagWithValue, TagTraduit, TagGoogleMaps, \
    TagGoogleMapsTraduit, GoogleException
from app.models.personne import PersonneTravel, PersonneHobby, Personne, \
    PersonneLiked, PersonneSearch
from app.views.common import LoginRequiredMixin, CommonView, HQFPaginator


class SearchView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'my_home/search/base.html'

    @staticmethod
    def clean_html(chaine, default=None):
        s = MLStripper()
        s.feed(chaine if chaine else '')
        s = s.get_data().replace('\n', ' ').replace('\r', '').strip()
        return s if s else default

    @staticmethod
    def clean_int(self, chaine, default=None):
        s = self.clean_html(chaine)
        if s is None:
            return default
        try:
            return int(s)
        except ValueError:
            return default

    def get_context_data(self, **kwargs):

        common = CommonView(self, **kwargs)
        context = super(SearchView, self).get_context_data(**kwargs)

        # -----------------------------------------------------
        # Analyse de tout ce qu'il y a dans le get pour faire la requête :
        g = self.request.GET
        travel = self.clean_html(g.get('travel'), '')
        s_dd = self.clean_int(self, g.get('date_start_1'), '**')
        s_mm = self.clean_int(self, g.get('date_start_0'), '**')
        s_yy = self.clean_int(self, g.get('date_start_2'), '-1')
        e_dd = self.clean_int(self, g.get('date_end_1'), '**')
        e_mm = self.clean_int(self, g.get('date_end_0'), '**')
        e_yy = self.clean_int(self, g.get('date_end_2'), '-1')

        nb_enfants = self.clean_int(self, g.get('nb_enfants'), -1)
        sexe = self.clean_int(self, g.get('sexe'), -1)
        langue = self.clean_int(self, g.get('langue'), -1)
        niveau_etudes = self.clean_int(self, g.get('niveau_etudes'), -1)
        employer_current = self.clean_html(g.get('employer_current'))
        employer_previous = self.clean_html(g.get('employer_previous'))
        profession = self.clean_int(self, g.get('profession'), -1)
        est_fumeur = self.clean_int(self, g.get('est_fumeur'), -1)
        custom_zodiac_sign = self.clean_int(
            self, g.get('custom_zodiac_sign'), -1)

        def mk_datepartial(yy, mm, dd):
            if yy != '-1':
                ok = '{:0>4}-{:0>2}-{:0>2}'.format(yy, mm, dd)
                try:
                    parse_date_partial(ok)
                    return ok
                except ValidationError:
                    self.request.session['message'] = (
                        _('Bad dates'),
                        _("Click here to hide this message"))
            return None

        # si on précise le jour SANS le mois, virer le jour :
        if (s_dd != '**') and (s_mm == '**'):
            s_dd = '**'
        if (e_dd != '**') and (e_mm == '**'):
            e_dd = '**'

        # Vérification que les dates sont valables :
        s = mk_datepartial(s_yy, s_mm, s_dd)
        if not s:  # Forcer les combos jj et mm à vide
            s_dd = '**'
            s_mm = '**'

        e = mk_datepartial(e_yy, e_mm, e_dd)
        if not e:  # Forcer les combos jj et mm à vide
            e_dd = '**'
            e_mm = '**'

        if not self.request.session.get('message'):
            # Ok, dates valides (sinon message venant de mk_datepartial())
            if s and e and (s > e):
                # Remettre les dates dans l'ordre :
                s, e = e, s
                s_dd, e_dd = e_dd, s_dd
                s_mm, e_mm = e_mm, s_mm
                s_yy, e_yy = e_yy, s_yy

        # ---------------------------------------------------------------------
        # Construction de la requête finale, prise en compte de tous les champs
        q = Q()
        if s:
            q &= Q(date_start__gte=s)
        if e:
            q &= Q(date_end__lte=e)

        age = self.clean_int(self, g.get('age'), '-1')
        if age in PersonneEnums.TAB_AGE_ECART:
            ecart = PersonneEnums.TAB_AGE_ECART[age]
            n = now()
            q &= Q(personne__date_naissance__lte=n.replace(
                year=n.year - ecart['min']))
            if ecart['max'] > 0:
                q &= Q(personne__date_naissance__gte=
                       n.replace(year=n.year - ecart['max']))

        if nb_enfants >= 0:
            q &= Q(personne__nb_enfants__exact=nb_enfants)
        else:
            nb_enfants = None
        if sexe >= 0:
            q &= Q(personne__sexe__exact=sexe)
        else:
            sexe = None
        if langue >= 0:
            q &= Q(personne__langue__exact=langue)
        else:
            langue = None
        if niveau_etudes >= 0:
            q &= Q(personne__niveau_etudes__exact=niveau_etudes)
        else:
            niveau_etudes = None
        if employer_current:
            q &= Q(personne__employer_current__exact=employer_current)
        else:
            employer_current = None
        if employer_previous:
            q &= Q(personne__employer_previous__exact=employer_previous)
        else:
            employer_previous = None
        if profession >= 0:
            q &= Q(personne__profession__exact=profession)
        else:
            profession = None
        if est_fumeur >= 0:
            q &= Q(personne__est_fumeur__exact=est_fumeur)
        else:
            est_fumeur = None
        if custom_zodiac_sign >= 0:
            q &= Q(personne__custom_zodiac_sign__exact=custom_zodiac_sign)
        else:
            custom_zodiac_sign = None

        programmes2 = [int(l) for l in g.getlist('programmes2')]
        activites2 = [int(l) for l in g.getlist('activites2')]
        hobbies2 = [int(l) for l in g.getlist('hobbies2')]
        types_permis2 = [int(l) for l in g.getlist('types_permis2')]
        personnalites2 = [int(l) for l in g.getlist('personnalites2')]
        langues2 = [int(l) for l in g.getlist('langues2')]

        if len(q):
            q = q & Q(personne__est_active=True) & Q(personne__est_detruit=None)

        print(q)

        if travel:
            results = []
            # There's a place to search
            v = TagGoogleMapsTraduit.objects.filter(
                langue__locale__exact=common.infos['locale'],
                formatted_address__iexact=travel
            )
            if len(v) == 0:
                # Not already cached -> ask google and add to my db cache
                try:
                    print('{} not found -> asking google...'.format(travel))
                    TagGoogleMapsTraduit.make_cache_via_google_maps(
                        text=travel, locale=common.infos['locale'])
                    # Get it again so we're sure everything's fine:
                    v = TagGoogleMapsTraduit.objects.filter(
                        langue__locale__exact=common.infos['locale'],
                        formatted_address__iexact=travel
                    )
                    print('cache done not we have:')
                    print(' // '.join([str(p) for p in v]))
                except GoogleException as e:
                    self.request.session['message'] = [
                        _("Nothing found"),
                        _("Google didn't find a town/country with this name"),
                        _("Click here to hide this message")]

            # save the search only if town and it's not another page:
            if len(v):
                tab = [p.tag_google_maps.pk for p in v]
                # register
                if g.get('page', '1') == '1':
                    # remember that search:
                    for p in v:
                        # p = TagGoogleMapsTraduit
                        # -> add the search
                        ps = PersonneSearch.objects.create(
                            personne=common.infos['personne'],
                            search=p)
                        ps.save()

                results = PersonneTravel.objects.filter(
                    ~Q(personne=common.infos['personne']) &
                    Q(travel__tag_google_maps__in=tab) & q)
        elif s or e or len(q):
            results = PersonneTravel.objects.filter(
                (~Q(personne=common.infos['personne'])) & q)
        else:
            results = None

        # mémo pour me souvenir de comment n'avoir que les ids des personnes,
        # et non plus les voyages :
        if results is not None:
            if isinstance(results, models.QuerySet):
                # pour faire "tous les choix PRÉSENTS,
                # le "__in=" ne fonctionne pas, il fait un "OU", alors que
                # je veux un "ET". Solution = ".filter()" enchaînés :
                for pk in [int(l) for l in activites2]:
                    results = results.filter(personne__activites2__pk=pk)
                for pk in [int(l) for l in programmes2]:
                    results = results.filter(personne__programmes2__pk=pk)
                for pk in [int(l) for l in hobbies2]:
                    results = results.filter(personne__hobbies2__pk=pk)
                for pk in [int(l) for l in types_permis2]:
                    results = results.filter(personne__types_permis2__pk=pk)
                for pk in [int(l) for l in personnalites2]:
                    results = results.filter(personne__personnalites2__pk=pk)
                for pk in [int(l) for l in langues2]:
                    results = results.filter(personne__langues2__pk=pk)
                results = set(results.values_list('personne', flat=True))

            results = Personne.objects.filter(pk__in=results) \
                .order_by('-user__last_login', '-date_creation')

            context['search_results_title'] = _(
                'Results matching with your criterias '
                'found: <b>{}</b>').format(results.count())
            # Pagination des résultats
            if common.infos['personne'].id == 585:
                max_page = 50
            else:
                max_page = 9
            paginator = HQFPaginator(results, max_page)
            try:
                page = int(self.request.GET.get('page', 1))
            except ValueError:
                page = 1
            try:
                paginator.set_around(page, 3)
                results = paginator.page(page)
            except PageNotAnInteger:
                # Si page n'est pas un entier, renvoyer la page 1.
                results = paginator.page(1)
            except EmptyPage:
                # Si page hors limites (ex. 9999) renvoyer la dernière page.
                results = paginator.page(paginator.num_pages)

            context['search_results'] = results

        # Mémo si plusieurs valeurs
        # known_languages = self.request.GET.getlist('known_languages')

        context['common'] = common.infos
        context['titre'] = _('Search')
        # reconstruire la forme en ré-injectant les données du GET :
        context['form_basique'] = SearchBasicForm({
            'travel': travel if travel else '',
            'date_start': '{}-{}-{}'.format(s_yy, s_mm, s_dd),
            'date_end': '{}-{}-{}'.format(e_yy, e_mm, e_dd),
        })
        # Ajouter une erreur :
        # context['form_basique'].add_error('travel', u'Erreur test')

        context['form_avancee'] = SearchAdvancedForm(initial={
            'travel': travel if travel else '',
            'date_start': '{}-{}-{}'.format(s_yy, s_mm, s_dd),
            'date_end': '{}-{}-{}'.format(e_yy, e_mm, e_dd),
            'nb_enfants': nb_enfants,
            'sexe': sexe,
            'langue': langue,
            'niveau_etudes': niveau_etudes,
            'employer_current': employer_current,
            'employer_previous': employer_previous,
            'profession': profession,
            'est_fumeur': est_fumeur,
            'custom_zodiac_sign': custom_zodiac_sign,
            'programmes2': programmes2,
            'activites2': activites2,
            'hobbies2': hobbies2,
            'types_permis2': types_permis2,
            'personnalites2': personnalites2,
            'langues2': langues2,
            'age': age,
        })

        p = Personne.objects.get(user=self.request.user)
        context['liked_person'] = [liked_p.dst
                                   for liked_p in PersonneLiked.objects.filter(
                                       activite__isnull=True,
                                       src=p,
                                       date_v_fin__isnull=True
                                   )]

        # Comme un peu partout ailleurs, effacer le message s'il y en avait un :
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context


