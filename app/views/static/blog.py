# coding=UTF-8


from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views import generic

from app.models.blog import BlogTraduit
from app.models.personne import Activite
from app.views.common import CommonView


class BlogView(generic.TemplateView):
    template_name = 'static/blog.html'

    def get_context_data(self, **kwargs):
        common = CommonView(self)
        context = super(BlogView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        # aller chercher tous "blogs" de la langue en cours
        ids = Activite.objects.filter(
            Q(activite__exact=Activite.ACTIVITE_BLOG,
              blog_traduit__locale=common.infos['locale'])
        ).values_list('blog_traduit__pk')

        context['blogs'] = BlogTraduit.objects.filter(pk__in=ids).order_by(
            '-blog__ordre_si_top',
            '-blog__date_publication',
            '-blog__date_last_modif')

        context['blog_title'] = _('Cogofly - Blog')
        context['blog_contact_us'] = _(
            'If you require any more information or have any questions, '
            'please feel free to contact us by email by clicking '
            '<a href="mailto:cogofly@gmail.com" target="_blank">'
            'here '
            '</a>')
        return context
