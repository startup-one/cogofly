# coding=UTF-8



from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic

from app.forms.profile.profile_newsletter_configuration import \
    ProfileNewsletterConfigurationForm
from app.models.personne import Personne
from app.views.common import LoginRequiredMixin
from django.utils.translation import ugettext as _


class NewsletterConfigurationView(LoginRequiredMixin, generic.FormView):
    template_name = 'my_home/profile/base.html'
    form_class = ProfileNewsletterConfigurationForm
    success_url = reverse_lazy('my_home_profile_edit')

    def get_context_data(self, **kwargs):
        context = super(NewsletterConfigurationView,
                        self).get_context_data(**kwargs)
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def get_object(self):
        try:
            return Personne.objects.get(user=self.request.user)
        except Personne.DoesNotExist:
            return None

    def form_valid(self, form):
        conf = form.cleaned_data.get('newsletter_configuration', None)
        if conf:
            try:
                p = self.get_object()
                conf = int(conf)
            except ValueError:
                return redirect(self.success_url)

            print("conf valide : ", conf)
            print("sauvegarde : ")
            p.newsletter_configuration = conf
            p.save()
            self.request.session['message'] = [
                _("Newsletter configuration updated"),
                _("Your newsletter configuration has been updated."),
                _("Click here to hide this message")]
        return super(NewsletterConfigurationView, self).form_valid(form)
