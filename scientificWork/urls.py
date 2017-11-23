#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from scientificWork import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^competitions$', views.competitions, name='competitions'),
    url(r'^publications$', views.publications, name='publications'),
    url(r'^rads$', views.rads, name='rads'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^staff/$', views.staff, name='staff'),
    url(r'^lk/$', views.lk, name='lk'),
    url(r'^addPublication/$', views.addPublication, name='addPublication'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
)


