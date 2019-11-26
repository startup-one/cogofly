# coding=UTF-8

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.shortcuts import redirect

from app.forms.message_send import MessageSendForm
from app.models.conversation import Conversation
from app.models.personne import Personne, PersonneRelation
from app.models.personne_enums import PersonneEnums
from app.views.common import CommonView, HQFPaginator
from app.views.my_home.post_message_view import PostMessageView


class ContactDetailView(PostMessageView):
    template_name = 'my_home/contact_detail.html'

    # (!) seule manière "propre" d'écraser 'url_redirect' du parent afin de
    #     renvoyer une valeur dynamiquement : la transformer en propriété :
    @property
    def url_redirect(self):
        return self.request.build_absolute_uri(self.request.path)

    def get_context_data(self, **kwargs):
        # 'contact_id' = param de l'URL => dans kwargs => faire suivre kwargs :
        common = CommonView(self, **kwargs)
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        try:
            contact = Personne.objects.get(pk=kwargs['contact_id'])
        except Personne.DoesNotExist:
            # pas d'index 'contact' crée -> gestion plus tard via get()
            return context

        context['contact'] = contact

        # pagination for contacts
        contact_contacts = contact.contacts
        # Pagination
        paginator = HQFPaginator(contact_contacts, 6)
        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1
        try:
            paginator.set_around(page, 3)
            contact_contacts = paginator.page(page)
        except PageNotAnInteger:
            # Si page n'est pas un entier, renvoyer la page 1.
            contact_contacts = paginator.page(1)
        except EmptyPage:
            # Si page est hors limites, (ex. 9999), renvoyer la dernière page.
            contact_contacts = paginator.page(paginator.num_pages)
        context['contact_contacts'] = contact_contacts

        context['form_send_message'] = MessageSendForm(obj_bd=contact,
                                                       champ='id_personne')
        p = common.infos['personne']
        convs = Conversation.between(p, contact)
        if len(convs):  # get() = pour avoir un objet (!= QuerySet)
            # normalement qu'une seule conversation avec des messages :
            c = Conversation.objects.get(pk=convs[0])
            context['conversation'] = c
            context['conversation_form'] = MessageSendForm(
                obj_bd=c, champ='id_conversation')

        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def get(self, request, *args, **kwargs):
        retour = super(ContactDetailView, self).get(request, *args, **kwargs)
        if not retour.context_data.get('contact'):  # pas trouvé = hack obligé
            return redirect('my_home_index')
        return retour

