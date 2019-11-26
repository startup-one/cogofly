# coding=UTF-8



from django.contrib import auth
from django.urls import reverse_lazy, resolve, Resolver404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.forms import LoginForm
from app.views.common import CommonView
from axes.decorators import axes_dispatch


class LoginView(generic.FormView):
    template_name = 'my_home/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('my_home_index')


    def get_context_data(self, **kwargs):
        common = CommonView(self)
        context = super(LoginView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        if self.request.session.get('message'):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        context['titre'] = _('Login')
        context['form'] = LoginForm()
        return context

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            # déconnecter que si pas reset de password :
            if not request.session.get('reset_password'):
                auth.logout(request)
                return redirect('%s?next=%s' % (reverse_lazy('my_home_index'),
                                                request.path))

        if request.GET.get('next') is None:
            # redirect pour qu'il y ait ajout automatique de next
            # (sinon login via google / facebook renvoie sur '/' )
            return redirect(reverse_lazy('my_home_index'))

        # si on se connecte via google ou facebook, url_back est utilisée :
        request.session['url_back'] = 'my_home_index'
        # (!) si via google ou facebook il oublie la langue en cours !
        request.session['url_language'] = translation.get_language()
        return super(LoginView, self).get(request, *args, **kwargs)

    # @axes_dispatch
    def form_valid(self, form):
        # username = form.cleaned_data['username']

        email_or_username = form.cleaned_data['email_or_username']
        password = form.cleaned_data['password']
        # hack pour faire un fake username
        username = email_or_username.replace('@', '_at_')

        user = auth.authenticate(username=username, password=password)
        if user is None:
            form.add_error(None, _('Invalid email or nick or password'))
            return super(LoginView, self).form_invalid(form)
        if not user.is_active:
            form.add_error(None, _('This account is not activated.'))
            return super(LoginView, self).form_invalid(form)
        auth.login(self.request, user)
        nxt = self.request.GET.get('next')
        if nxt:
            try:
                resolve(nxt)
                return HttpResponseRedirect(nxt)
            except Resolver404 as e:
                print(e)
        return super(LoginView, self).form_valid(form)


