# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, TemplateView

from core.models import Role
from news.feeds import NewsFeed

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/registration$', 'core.views.registration', name='registration'),
    url(r'^auth/login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^auth/logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^auth/password_reset$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^auth/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^auth/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^auth/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^admin/', include(admin.site.urls), name="admin"),

    url('^$', direct_to_template, {'template': 'index.html'}),

)
