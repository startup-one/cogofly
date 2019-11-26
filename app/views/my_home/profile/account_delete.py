# coding=UTF-8


from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.utils.timezone import make_aware
from django.views import generic
from django.utils.datetime_safe import datetime as django_datetime

from app.forms.profile.profile_delete import ProfileDeleteForm
from app.models.personne import Personne
from app.views.common import LoginRequiredMixin, CommonView


class AccountDeleteView(LoginRequiredMixin, generic.FormView):
    template_name = 'my_home/profile/base.html'
    form_class = ProfileDeleteForm
    success_url = reverse_lazy('my_home_profile_edit')

    def get_context_data(self, **kwargs):
        # 'contact_id' = param de l'URL => dans kwargs => faire suivre kwargs :
        common = CommonView(self, **kwargs)
        context = super(AccountDeleteView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def get_object(self, queryset=None):
        p = Personne.objects.filter(
            user__pk__exact=self.request.user.pk
        ).all()
        return p[0] if len(p) else None

    def form_valid(self, form):
        # (!!) User est une clé étrangère = pas mis à jour automatiquement :
        i_agree_delete = form.cleaned_data.get('i_agree_delete')
        if i_agree_delete:
            self.request.session['message'] = [
                _('Account deleted'),
                _('You have just deleted your account.'),
                _('Please feel free to come back in the near future '
                  'and check out any new features which, we hope, '
                  'will persuade you to share the adventure with us again.'),
                _('We would like to take this opportunity to thank you '
                  'for using Cogofly and hope to see you again very soon.'),
                _('Click here to hide this message')]
            p = self.get_object()
            u = User.objects.get(pk=p.user.pk)
            p.est_active = False
            p.est_detruit = make_aware(django_datetime.now())
            reason_delete = form.cleaned_data.get('reason_delete')
            p.reason_delete = reason_delete if reason_delete else None
            p.save()
            if 'development' not in self.request.META['HTTP_HOST']:
                EmailMessage(
                    subject=_('Account deleted'),
                    body='{}\n{}\n{}\n{}'.format(
                        _('You have just deleted your account.'),
                        _('We would like to take this opportunity to thank '
                          'you for using Cogofly and hope to see '
                          'you again very soon.'),
                        _('Please feel free to come back in the near future '
                          'and check out any new features which, we hope, '
                          'will persuade you to share the adventure '
                          'with us again.'),
                        _('Thank you!'),
                    ),
                    from_email='register@cogofly.com',
                    to=[u.email],
                    bcc=[]).send()
                EmailMessage(
                    subject=_('Account deleted'),
                    body='{}\n{}'.format(
                        _('{} (email: {}) '
                          'has just deleted his/her account.').format(
                            p.full_name(), u.email
                        ),
                        _('The reason for deletion is: {}').format(
                            reason_delete if reason_delete
                            else _('not precised')
                        ),
                    ),
                    from_email='contact@cogofly.com',
                    # to=[u'cogofly+support@gmail.com'],
                    bcc=[]).send()

            p.user.last_name = 'DELETE_{}'.format(
                p.user.last_name if p.user.last_name else ''
            )
            p.user.first_name = 'DELETE_{}'.format(
                p.user.first_name if p.user.first_name else ''
            )
            p.user.email = 'DELETE_{}'.format(
                p.user.email if p.user.email else ''
            )
            p.save()

        else:
            self.request.session['message'] = (
                _('No action!'),
                _('If you want to delete your account,'
                  'please check "Yes".'))
        return super(AccountDeleteView, self).form_valid(form)
#
