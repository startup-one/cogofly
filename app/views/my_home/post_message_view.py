# coding=UTF-8



from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.html import MLStripper
from django.utils.translation import ugettext as _
from django.views import generic

from app.models.conversation import Conversation, Message
from app.models.personne import Personne, Activite
from app.views.common import LoginRequiredMixin


class PostMessageView(LoginRequiredMixin, generic.TemplateView):
    """
    Vue utilisée par celles qui gèrent l'envoi de message via les formulaires
    Au moment où j'écris il y a index.py, contact_detail.py et index.py
    """
    url_redirect = None

    def get_context_data(self, **kwargs):
        context = super(PostMessageView, self).get_context_data(**kwargs)
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def post(self, request, *args, **kwargs):
        # Suppression de toutes les tentatives de hack :
        if not request.POST.get('csrfmiddlewaretoken'):
            return redirect(self.url_redirect)

        # ! Comparaison codée en dur, je ne sais pas comment faire autrement :
        if request.POST['csrfmiddlewaretoken'] != csrf(request)['csrf_token']:
            return redirect(self.url_redirect)

        if request.POST.get('message'):
            dst = None

            # p = Personne liée au User en cours
            p = Personne.objects.get(user=self.request.user)

            # c = conversation en cours
            c = None

            # Nettoyage du message :
            s = MLStripper()
            s.feed(request.POST['message'])
            message = s.get_data()\
                .replace('\n', ' ').replace('\r', '')

            # ! ici deux posts possibles : Activite ou Conversation
            if request.POST.get('id_activite'):
                try:
                    id_activite = int(request.POST['id_activite'])
                except ValueError:
                    id_activite = None
                if isinstance(id_activite, int):
                    a = Activite.objects.get(pk=id_activite)
                    if a.relation:
                        dst = a.relation.src
                    else:
                        dst = a.travel.personne
            elif request.POST.get('id_conversation'):
                try:
                    id_conversation = int(request.POST['id_conversation'])
                except ValueError:
                    id_conversation = None
                if isinstance(id_conversation, int):
                    c = Conversation.objects.get(pk=id_conversation)
                    print(c)
                    m = Message.objects.filter(conversations__exact=c) \
                        .values_list('src', 'dst')
                    print(m)

                    # réduire groupes de valeurs en un tableau unique :
                    # -> ids de *tous* les participants *sauf* user actuel
                    m = [a for a in sorted(set().union(*m)) if a != p.pk]
                    print(request.POST)
                    print(m)

                    # au moment où j'écris, uniquement *deux* participants
                    # moins le user en cours :
                    if len(m) == 1:
                        dst = Personne.objects.get(pk=m[0])

            elif request.POST.get('id_personne'):
                try:
                    id_personne = int(request.POST['id_personne'])
                except ValueError:
                    id_personne = None
                if isinstance(id_personne, int):
                    try:
                        dst = Personne.objects.get(pk=id_personne)
                        # (!) Reste à faire côté sécurité : vérifier que
                        #     dst est vraiment un contact du User en cours
                    except Personne.DoesNotExist:  # hack
                        dst = None

            if isinstance(dst, Personne):
                # Ok, on sait à qui écrire :
                # conversation peut être déjà calculée avant -> vérifier :
                if isinstance(c, Conversation):
                    m = Message.objects.create(src=p, dst=dst,
                                               message=message)
                    m.save()
                    c.messages.add(m)
                    c.save()
                else:  # Envoyer un message à l'autre personne :
                    Conversation.add_message(p, dst, message)

                self.request.session['message'] = (
                    _('Message sent'),
                    _('Click to hide'))

        elif request.POST.get('message_id'):
            # pas de message dans le POST, message_id = "marquer comme lu"
            try:
                message_id = int(request.POST['message_id'])
            except ValueError:
                message_id = None
            if isinstance(message_id, int):
                try:
                    m = Message.objects.get(pk=message_id)
                    m.is_read = True
                    m.save()
                except Message.DoesNotExist:
                    pass

        return redirect(self.url_redirect)


