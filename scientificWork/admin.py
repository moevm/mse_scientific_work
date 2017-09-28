#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

# Подключаем наши модели в админку сайта
from scientificWork.models import Publication, Participation, Rand, UserProfile

# Регистрируем импортированную модель в админку
admin.site.register(Publication)
admin.site.register(Rand)
admin.site.register(Participation)
admin.site.unregister(User)
admin.site.register(UserProfile)
