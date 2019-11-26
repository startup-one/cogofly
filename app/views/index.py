# coding=UTF-8


from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views import generic

from app.views.common import CommonView


class IndexView(generic.TemplateView):
    template_name = 'beta/index.html'

    def get(self, req, *args, **kwargs):
        common = CommonView(self)
        return render(req, self.template_name, {
            'common': common.infos,
            'titre': _('Home')})
