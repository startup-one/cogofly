# coding=UTF-8


from django.views import generic
from app.views.common import LoginRequiredMixin, CommonView


class AccountDesactivatedView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'my_home/profile/redirect/account_desactivated.html'

    def get_context_data(self, **kwargs):
        # 'contact_id' = param de l'URL => dans kwargs => faire suivre kwargs :
        common = CommonView(self, **kwargs)
        context = super(AccountDesactivatedView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context
