# coding=UTF-8


from django.contrib import auth
from django.urls import reverse_lazy, resolve, Resolver404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.forms import LoginForm
from app.views.common import CommonView


class LogoutView(generic.View):

    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse_lazy('app_index'))


