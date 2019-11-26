# coding=UTF-8

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _

from app.forms.message_send import MessageSendForm
from app.models.conversation import Conversation, Message
from app.models.personne import Personne, PersonneRelation, Activite
from app.models.personne_enums import PersonneEnums
from app.views.common import CommonView, HQFPaginator
from app.views.my_home.post_message_view import PostMessageView


class NotificationsView(PostMessageView):
    template_name = 'my_home/notifications/base.html'
    url_redirect = 'my_home_notifications'

    def get_context_data(self, **kwargs):
        common = CommonView(self, **kwargs)
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context['common'] = common.infos

        # Pagination : écraser les likes
        likes = context['common']['notifications']['likes']
        paginator = HQFPaginator(likes, 5)
        try:
            page = int(self.request.GET.get('p_like', 1))
        except ValueError:
            page = 1
        try:
            paginator.set_around(page, 3)
            likes = paginator.page(page)
        except PageNotAnInteger:
            # Si page n'est pas un entier, renvoyer la page 1.
            likes = paginator.page(1)
        except EmptyPage:
            # Si page est hors limites, (ex. 9999), renvoyer la dernière page.
            likes = paginator.page(paginator.num_pages)
        context['common']['notifications']['likes'] = likes

        context['titre'] = _('Notifications')
        p = common.infos['personne']

        convs_non_lues = Conversation.objects.filter(
            Q(messages__dst=p, messages__is_read=False,
              messages__date_v_fin__isnull=True)).distinct()
        context['conversations'] = [
            {'form': MessageSendForm(obj_bd=c, champ='id_conversation'),
             'conversation': c}
            for c in convs_non_lues]

        l = []
        for m in Message.objects.filter(dst=p, dst_visible=True)\
                .order_by('date_last_modif'):
            for c in m.conversations.all().exclude(pk__in=convs_non_lues):
                if c.pk not in l:
                    l.append(c.pk)
        convs_lues = [Conversation.objects.get(pk=int(pk)) for pk in l]

        context['conversations_lues'] = [
            {'form': MessageSendForm(obj_bd=c, champ='id_conversation'),
             'conversation': c}
            for c in convs_lues]

        # Pagination
        paginator = HQFPaginator(context['conversations_lues'], 8)
        try:
            page = int(self.request.GET.get('p_convs', 1))
        except ValueError:
            page = 1
        try:
            paginator.set_around(page, 3)
            context['conversations_lues'] = paginator.page(page)
        except PageNotAnInteger:
            # Si page n'est pas un entier, renvoyer la page 1.
            context['conversations_lues'] = paginator.page(1)
        except EmptyPage:
            # Si page est hors limites, (ex. 9999), renvoyer la dernière page.
            context['conversations_lues'] = paginator.page(paginator.num_pages)

        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        # ! Comparaison codée en dur, je ne sais pas comment faire autrement :
        if post['csrfmiddlewaretoken'] == csrf(request)['csrf_token']:

            p_src = Personne.objects.get(user=self.request.user)
            id_dst = None
            p_dst = None
            raison = None
            msg_head = None
            msg_to_show = None
            msg_to_send = None
            type_relation = PersonneEnums.RELATION_AMI
            if post.get('id_personne_accept'):
                try:
                    id_dst = int(post['id_personne_accept'])
                except ValueError:
                    return redirect(self.url_redirect)

                p_dst = Personne.objects.get(pk=id_dst)
                msg_head = _('Invitation accepted')
                msg_to_show = _("{} has been notified that you accepted the "
                                "invitation").format(p_dst.full_name())
                msg_to_send = _("I've accepted your invitation")

            elif post.get('id_personne_refused') and post.get('raison_refus'):
                try:
                    id_dst = int(post['id_personne_refused'])
                    raison = int(post['raison_refus'])
                except ValueError:
                    return redirect(self.url_redirect)

                p_dst = Personne.objects.get(pk=id_dst)
                msg_head = _('Invitation declined')
                msg_to_show = _("{} has been notified that you declined the "
                                "invitation").format(p_dst.full_name())
                msg_to_send = _("I've declined your invitation.\n"
                                "The reason is: {}").format(
                    PersonneEnums.TAB_INVITATION[raison])
                type_relation = PersonneEnums.RELATION_INVITATION_REFUSEE

            if id_dst and p_dst:

                PersonneRelation.objects.filter(
                    (Q(src=p_src) & Q(dst=p_dst)) |
                    (Q(src=p_dst) & Q(dst=p_src))
                ).update(type_relation=type_relation,
                         raison_refus=raison)
                if raison is None:
                    # Accepté, donc ajout de l'activité "nouvelle relation" :
                    p_r = PersonneRelation.objects.get(src=p_src, dst=p_dst)
                    Activite.objects.create(
                        activite=Activite.ACTIVITE_AJOUT_RELATION,
                        relation=p_r)
                    Activite.objects.create(
                        activite=Activite.ACTIVITE_AJOUT_RELATION,
                        relation=p_r.opposite)

                self.request.session['message'] = [
                    msg_head, msg_to_show,
                    _('Click here to hide this message')]

                # Envoyer un message à l'autre personne :
                Conversation.add_message(p_src, p_dst, msg_to_send)

                return redirect(self.url_redirect)

        return super(NotificationsView, self).post(request, *args, **kwargs)
