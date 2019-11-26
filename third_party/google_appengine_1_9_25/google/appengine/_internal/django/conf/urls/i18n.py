
from google.appengine._internal.django.conf.urls.defaults import *
from django.conf.urls import url

urlpatterns = ['',
    url(r'^setlang/$', 'django.views.i18n.set_language'),
]
