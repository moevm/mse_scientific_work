# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from scientificWork.models import *
from django.test.client import Client
from django.contrib.auth.models import User

c = Client()

# Тесты авторизации
class AuthorizationTest(TestCase):
    def setUp(self):
        # Создаем активного пользователя
        self.username = 'admin'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username,
        'mail@example.com',
        self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        # Создаем неактивного пользователя
        self.username2 = 'adminBloked'
        self.user2 = User.objects.create_user(self.username2,
        'mail@example.com',
        self.password)
        self.user2.is_staff = True
        self.user2.is_superuser = True
        self.user2.is_active = False
        self.user2.save()

    # тест на авторизацию с правильным логином и паролем
    def test_success(self):
        response = c.post('/scientificWork/login/', {'username': 'admin', 'password': 'secret'})
        self.assertRedirects(response, "/scientificWork/", status_code=302, target_status_code=200, msg_prefix='')

    # тест на авторизацию с неправильным логином
    def test_bad_login(self):
        response = c.post('/scientificWork/login/', {'username': 'admin2', 'password': 'secret'})
        self.assertEqual(response.content, "Invalid login details supplied.")

    # тест на авторизацию с неправильным паролем
    def test_bad_password(self):
        response = c.post('/scientificWork/login/', {'username': 'admin', 'password': 'secret1'})
        self.assertEqual(response.content, "Invalid login details supplied.")

    # тест на авторизацию неактивного пользователя
    def test_inactive_user(self):
        response = c.post('/scientificWork/login/', {'username': 'adminBloked', 'password': 'secret'})
        self.assertEqual(response.content, "Your  account is disabled.")


# Тесты на получение страниц
class GetPagesTest(TestCase):
	# тест получения главной страницы
    def test_home_page(self):
        response = c.get('/scientificWork/')
        self.assertEqual(response.status_code, 200)

    # тест получения страницы Участие в конференциях/семинарах
    def test_competitions_page(self):
        response = c.get('/scientificWork/competitions')
        self.assertEqual(response.status_code, 200)

    # тест получения страницы Публикации
    def test_publications_page(self):
        response = c.get('/scientificWork/publications')
        self.assertEqual(response.status_code, 200)

    # тест получения страницы НИОКР
    def test_rads_page(self):
        response = c.get('/scientificWork/rads')
        self.assertEqual(response.status_code, 200)