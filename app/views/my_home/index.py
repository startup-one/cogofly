# coding=UTF-8

import copy

from django.core.paginator import PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _

from app.forms.comment_send import CommentSendForm
from app.forms.express_yourself import ExpressYourselfForm
from app.forms.message_send import MessageSendForm
from app.models.personne import Personne, Activite, PersonneLiked, \
    ActiviteComments, ActiviteExpressyourself, PersonneTravel
from app.models.publicite import Publicite
from app.views.common import CommonView, HQFPaginator
from app.views.common_mixins import PubliciteMixin, ActivitesMixin, \
    ProgressionMixin
from app.views.my_home.post_message_view import PostMessageView


class IndexView(PubliciteMixin, ActivitesMixin, ProgressionMixin,
                PostMessageView):
    template_name = 'my_home/index.html'
    url_redirect = 'my_home_index'

    def get_context_data(self, **kwargs):
        common = CommonView(self)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('Home')
        p = Personne.objects.get(user=self.request.user)

        context['activites'] = self.activites(p, common.infos['locale'])

        context['liked'] = [
            liked.activite
            for liked in PersonneLiked.objects.filter(
                activite__in=context['activites'],
                liked__exact=True,
                src=p,
                date_v_fin__isnull=True
            )]
        context['liked_person'] = [
            liked_p.dst
            for liked_p in PersonneLiked.objects.filter(
                activite__isnull=True,
                liked__exact=True,
                src=p,
                date_v_fin__isnull=True
            )]
        context['activites'] = [
            {'objet': a,
             'form': MessageSendForm(obj_bd=a, champ='id_activite'),
             'form_comment': CommentSendForm(obj_bd=a,
                                             champ='id_comment_activite'),
             'comments': ActiviteComments.objects.filter(activite_dst=a)
             }
            for a in context['activites']
            ]
        context['express_yourself'] = ExpressYourselfForm()

        # Pagination
        paginator = HQFPaginator(context['activites'], 8)
        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1
        try:
            paginator.set_around(page, 3)
            context['activites'] = paginator.page(page)
        except PageNotAnInteger:
            # If not integer, back to page 1.
            context['activites'] = paginator.page(1)
        except EmptyPage:
            # If out of bound (ex. 9999), send latest page
            context['activites'] = paginator.page(paginator.num_pages)

        # Message (if there's one)
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']

        # Publicités
        context['publicites_gauche'] = \
            self.publicites(Publicite.PUBLICITE_FIL_ACTUALITE_GAUCHE)
        context['publicites_droite'] = \
            self.publicites(Publicite.PUBLICITE_FIL_ACTUALITE_DROITE)

        # Travels
        if self.request.session.get('warn_no_travels', None) is None:
            self.request.session['warn_no_travels'] = True
            if PersonneTravel.objects.filter(
                    personne=p, date_v_fin__isnull=True).count() == 0:
                self.request.session['warn_no_travels'] = True
                context['warn_no_travels'] = True

        # Progression
        if self.request.session.get('progression', None) is None:
            self.request.session['progression'] = False
        if not self.request.session['progression']:
            self.request.session['progression'] = True
            context['progression'] = self.progression(self.request.user, p)

        return context

    def post(self, request, *args, **kwargs):
        # 4 mêmes lignes que dans le parent pour la sécurité:
        if not request.POST.get('csrfmiddlewaretoken'):
            return redirect(self.url_redirect)
        if request.POST['csrfmiddlewaretoken'] != csrf(request)['csrf_token']:
            return redirect(self.url_redirect)

        # Read fields if add comments:
        msg = request.POST.get('message')
        id_activite = request.POST.get('id_comment_activite')
        express_yourself = request.POST.get('express_yourself')
        if id_activite and msg:
            # arrivé ici, on a tout dans msg et id_activite, ajout :
            try:
                activite_dst = Activite.objects.get(pk=int(id_activite))
            except ValueError:
                return redirect(self.url_redirect)
            p = Personne.objects.get(user=self.request.user)
            ac = ActiviteComments.objects.create(
                personne=p, activite_dst=activite_dst, comment=msg
            )
            ac.save()
            activite = Activite.objects.create(
                activite=Activite.ACTIVITE_COMMENT,
                comment=ac
            )
            activite.save()

            self.request.session['message'] = (
                _('Comment added!'),
                _('Click to hide'))
            return redirect(self.url_redirect)
        elif express_yourself:
            a_ey = ActiviteExpressyourself.objects.create(
                personne=Personne.objects.get(user=self.request.user),
                message=express_yourself
            )
            Activite.objects.create(
                activite=Activite.ACTIVITE_EXPRESSYOURSELF,
                express_yourself=a_ey)

            self.request.session['message'] = (
                _('Added to your wall!'),
                _('From now on you can share it to your contacts!'),
                _('Click to hide'))
            return redirect(self.url_redirect)

        # (!) the parent handles *messages* adding, ALWAYS call it
        #     if there's not post handled here:
        return super(IndexView, self).post(request, *args, **kwargs)
