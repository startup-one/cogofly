# coding=UTF-8

from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.remarks import RemarksForm
from app.forms.testimony import TestimonyForm
from app.models.personne import Personne, Activite, ActiviteTestimony
from app.views.common import LoginRequiredMixin, CommonView


class RemarksAndTestimoniesView(LoginRequiredMixin, generic.TemplateView):
    """
    Vue utilisée par celles qui gèrent l'envoi
    - des remarques / suggestions
    - des témoignages
    """
    template_name = 'my_home/remarks_and_testimonies.html'
    url_redirect = 'my_home_remarks_and_testimonies'

    def get_context_data(self, **kwargs):
        common = CommonView(self, **kwargs)
        context = super(RemarksAndTestimoniesView,
                        self).get_context_data(**kwargs)
        context['common'] = common.infos
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']

        context['form_remarks'] = RemarksForm()
        context['form_testimonies'] = TestimonyForm()
        return context

    def post(self, request, *args, **kwargs):
        # Suppression de toutes les tentatives de hack :
        if not request.POST.get('csrfmiddlewaretoken'):
            return redirect(self.url_redirect)

        # ! Comparaison codée en dur, je ne sais pas comment faire autrement :
        if request.POST['csrfmiddlewaretoken'] != csrf(request)['csrf_token']:
            return redirect(self.url_redirect)

        # p = Personne liée au User en cours
        p = Personne.objects.get(user=self.request.user)
        remarks = request.POST.get('remarks')
        testimony = request.POST.get('testimony')
        testimony_show_name = request.POST.get('testimony_show_name', False)
        if remarks:
            if 'development' not in self.request.META['HTTP_HOST']:
                nom_user = ' '.join([self.request.user.first_name,
                                      self.request.user.last_name]).strip()
                if nom_user:
                    nom_user = '{} ({})'.format(nom_user,
                                                 self.request.user.email)
                email_subject = 'Cogofly : message de la part de {}'.format(
                    nom_user if nom_user else self.request.user.email)

                EmailMessage(subject=email_subject,
                             body=remarks,
                             from_email='support@cogofly.com',
                             to=['support@cogofly.com',
                                 'cogofly+support@gmail.com']).send()

            self.request.session['message'] = [
                _('Dear Member,'),
                '',
                _('Thanks for your email. '
                  'We acknowledge receipt of your message.'),
                _('Rest assured that your request is being dealt with,'
                  'and that you will receive a reply very shortly'),
                _('Please feel free to contact us should you have any further '
                  'questions.'),
                '',
                _('Kind regards, '),
                _('Cogofly Team. '),
                _('Click here to hide this message')]
            return redirect(self.url_redirect)

        if testimony:
            a_t = ActiviteTestimony.objects.create(
                personne=p, testimony=testimony,
                testimony_show_name=testimony_show_name,
            )
            a_t.save()
            activite = Activite.objects.create(
                activite=Activite.ACTIVITE_TESTIMONY,
                testimony=a_t,
            )
            activite.save()
            if 'development' not in self.request.META['HTTP_HOST']:
                nom_user = ' '.join([self.request.user.first_name,
                                      self.request.user.last_name]).strip()
                if nom_user:
                    nom_user = '{} ({})'.format(nom_user,
                                                 self.request.user.email)
                email_subject = 'Cogofly : témoignage de la part de {}'.format(
                    nom_user if nom_user else self.request.user.email)
                site_web = "{}://{}".format(
                    self.request.scheme, self.request.META['HTTP_HOST']
                )

                EmailMessage(subject=email_subject,
                             body='{}{}\n{}'.format(
                                 # lien vers l'admin / édition du témoignage :
                                 site_web,
                                 reverse('admin:app_activitetestimony_change',
                                         args=(a_t.pk,)),
                                 testimony, ),
                             from_email='contact@cogofly.com',
                             to=['contact@cogofly.com',
                                 'cogofly+testimony@gmail.com']).send()
            self.request.session['message'] = [
                _('Dear Member,'),
                '',
                _('Thanks for your testimony, '
                  'we appreciate.'),
                _('It will be, or not, very soon accepted by the moderator.'),
                _("Thanks again and don't forget to talk about "
                  "www.cogofly.com around you... One "
                  "Cogoflyer could be close to you."),
                '',
                _('Kind regards, '),
                _('Cogofly Team. '),
                _('Click here to hide this message')]

        return redirect(self.url_redirect)


