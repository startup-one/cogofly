# coding=UTF-8

from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils.translation import ugettext as _

from app.forms.message_send import MessageSendForm
from app.models.personne_enums import PersonneEnums
from app.views.common import CommonView, HQFPaginator
from app.views.my_home.post_message_view import PostMessageView


class IndexView(PostMessageView):
    template_name = 'my_home/contacts/index.html'
    url_redirect = 'my_home_contacts'

    def get_context_data(self, **kwargs):
        common = CommonView(self, **kwargs)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('Home')
        current = common.infos['personne']

        # À partir de là on a les id -> ressortir les personnes avec ces ids.

        # Pagination des résultats
        contacts = [
            {'form': MessageSendForm(obj_bd=p, champ='id_personne'),
             'contact': p, }
            for p in current.relations_of_type(PersonneEnums.RELATION_AMI)]
        paginator = HQFPaginator(contacts, 6)
        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1
        try:
            paginator.set_around(page, 3)
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # Si page n'est pas un entier, renvoyer la page 1.
            contacts = paginator.page(1)
        except EmptyPage:
            # Si page hors limites (ex. 9999) renvoyer la dernière page.
            contacts = paginator.page(paginator.num_pages)

        context['contacts'] = contacts

        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

