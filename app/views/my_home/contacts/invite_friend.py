# coding=UTF-8

import uuid

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms import InviteFriendForm
from app.models.personne import Personne, PersonneRelation
from app.models.personne_enums import PersonneEnums
from app.views.common import LoginRequiredMixin, CommonView


class InviteFriendView(LoginRequiredMixin, generic.FormView):
    template_name = 'my_home/contacts/invite.html'
    form_class = InviteFriendForm
    success_url = reverse_lazy('my_home_contacts_invite')

    def get_initial(self):
        """
        Attention, get_initial() sert à pré-remplir avec des valeurs
        les champs du formulaire via initial['nom_du_champ']
        Ici, ça prête à confusion car j'ai un champ de mon formulaire que
        j'ai appelé "message"...
        """
        initial = super(InviteFriendView, self).get_initial()
        # Pour re-remplir avec le message qui a été envoyé :
        msg = self.request.session.get('message_prefill', None)
        if msg:
            del self.request.session['message_prefill']
        else:
            msg = _('Hi,\n\n'
                    'Join me absolutely free on, www.cogofly.com, the new '
                    'community where you can find people you can trust and '
                    'never have to worry about travelling alone again.\n\n'

                    'Don\'t stay on your own...meet people close to home or '
                    'abroad and share your activities with them.\n\n'

                    'Weekends away, days out, even business trips…you can '
                    'envisage doing all of these with someone who potentially '
                    'shares the same socio-professional criteria, hobbies and '
                    'travel aspirations as you.\n\n'

                    'If you enjoy spending time on your own…you will no doubt '
                    'be inspired by other people’s experiences and be able to '
                    'share information via this new web platform... and why '
                    'not make the most of people’s recommendations.\n\n'
                    'Cogofly Team : Alone, we think...'
                    'Together, we get away!\n\n'

                    'PS. Once you’ve checked out the site and finalized your '
                    'subscription, please feel free to share this information '
                    'with, maybe, your entourage.\n\n')
        initial['message'] = msg
        return initial

    def get_context_data(self, **kwargs):
        common = CommonView(self)
        context = super(InviteFriendView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('Invite friends')
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def form_valid(self, form):
        # username = form.cleaned_data['username']
        prenom = form.cleaned_data['prenom']
        nom = form.cleaned_data['nom']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # hack pour faire un fake username
        username = email.replace('@', '_at_')
        # Si username déjà utilisé, erreur :
        if len(User.objects.filter(username__exact=username)):
            err = _('A user has already the same firstname and lastname')
            form.add_error('prenom', err)
            form.add_error('nom', err)
            return super(InviteFriendView, self).form_invalid(form)
        # Si email déjà utilisé, erreur :
        if len(User.objects.filter(email__exact=email)):
            form.add_error('email', _('This email is already used'))
            return super(InviteFriendView, self).form_invalid(form)

        password = str(uuid.uuid4()).replace('-', '')[:10]
        # Création de l'utilisateur :
        u_ami = User.objects.create_user(username=username, email=email,
                                         password=password,
                                         first_name=prenom, last_name=nom)
        u_ami.is_active = False
        u_ami.save()
        rand_str = str(uuid.uuid4())
        p_ami = Personne(user=u_ami, confirmation_code=rand_str,
                         champs_supplementaires='',
                         temporary_visible_password=password)
        p_ami.save()

        # Création de la relation "ami" :
        p_cur = Personne.objects.get(user=self.request.user)
        pr = PersonneRelation(
            type_relation=PersonneEnums.RELATION_AMI,
            src=p_cur, dst=p_ami
        )
        pr.save()

        if 'development' not in self.request.META['HTTP_HOST']:
            site_web = "{}://{}".format(
                self.request.scheme, self.request.META['HTTP_HOST']
            )
            invite = ' '.join([self.request.user.first_name,
                                self.request.user.last_name]).strip()
            if invite:
                invite = _('{} has invited you!').format(invite)
            else:
                invite = _("Cogofly invites you!")

            email_subject = '{} {}'.format(
                '{}, '.format(' '.join([nom, prenom]).strip())
                if prenom or nom else '',
                invite
            ).strip()

            t = _("\nTo validate your registration, "
                  "click on the following link:\n{}{}").format(
                      site_web, reverse('contact_register_validate',
                                        kwargs={'rand_str': rand_str}))
            email_message = message + t.encode('utf_8')
            EmailMessage(subject=email_subject,
                         body=email_message,
                         from_email='register@cogofly.com',
                         to=[email],
                         # bcc=[u'cogofly+register@gmail.com'],
                         ).send()

        self.request.session['message'] = [
            _('Thanks for sharing!'),
            _('An email has been sent to the email address you provided.'),
            _('Click here to hide this message')]
        self.request.session['message_prefill'] = message
        return super(InviteFriendView, self).form_valid(form)


