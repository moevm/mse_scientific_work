#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from report import *

from scientificWork.models import Publication, UserProfile


def index(request):
    return render(request, 'scientificWork/index.html')


def lk(request):
    o1 = Publication.objects.all()
    template = loader.get_template('scientificWork/lk.html')
    context = RequestContext(request, {
        'o1': o1,
    })
    return HttpResponse(template.render(context))


def competitions(request):
    return render(request, 'scientificWork/competitions.html')


def publications(request):
    o = Publication.objects.all()

    filters = []
    if request.method == 'GET' and request.GET.items():
        if 'bookName' in request.GET:
            if len(request.GET.get('bookName')) > 0:
                o = o.filter(bookName=request.GET.get('bookName'))
                filters += ['bookName']
        if 'author' in request.GET:
            o = o.filter(user__patronymic=request.GET.get('author'))
        if 'type' in request.GET:
            if request.GET.get('type') != "all":
                o = o.filter(typePublication=request.GET.get('type'))
                filters += ['type']
        if 'date' in request.GET:
            if len(request.GET.get('date')) > 0:
                o = o.filter(date=request.GET.get('date'))
                filters += ['date']
        if 'citing' in request.GET:
            o = o.filter(citingBase=request.GET.get('citing'))

    o1 = []
    for p in o:
        o2 = {}
        o2["bookName"] = p.bookName
        o2["author"] = p.user.patronymic
        o2["date"] = p.date
        o2["type"] = p.get_typePublication_display()
        o1 += [o2]
    template = loader.get_template('scientificWork/publications.html')
    context = RequestContext(request, {
        'o': o1,
    })
    print_peport_publications_docx(o1, filters)
    print_list_publications_xlsx(o1, filters)
    return HttpResponse(template.render(context))


def staff(request):
    s = UserProfile.objects.all()
    filters = []
    if request.method == 'GET' and request.GET.items():
        if 'academic_degree' in request.GET:
            if request.GET.get('academic_degree') != "all":
                s = s.filter(academic_degree=request.GET.get('academic_degree'))
                filters += ["academic_degree"]
        if 'type' in request.GET:
            if request.GET.get('type') != "all":
                s = s.filter(type=request.GET.get('type'))
                filters += ["type"]
        if 'name' in request.GET:
            if len(request.GET.get('name')) > 0:
                s = s.filter(patronymic=request.GET.get('name'))
                filters += ["name"]
        if 'contract_date' in request.GET:
            if len(request.GET.get('contract_date')) > 0:
                s = s.filter(contract_date=request.GET.get('contract_date'))
                filters += ["contract_date"]
        if 'academic_status' in request.GET:
            if request.GET.get('academic_status') != "all":
                s = s.filter(academic_status=request.GET.get('academic_status'))
                filters += ["academic_status"]
    s1 = []
    for x in s:
        s2 = {}
        s2["type"] = x.get_type_display()
        s2["academic_degree"] = x.get_academic_degree_display()
        s2["name"] = x.patronymic
        s2["contract_date"] = x.contract_date
        s2["academic_status"] = x.get_academic_status_display()
        s1 += [s2]

    template = loader.get_template('scientificWork/staff.html')
    context = RequestContext(request, {
        's': s1,
    })

    print_peport_staff_docx(s1, filters)
    print_list_staff_xlsx(s1, filters)

    return HttpResponse(template.render(context))


def rads(request):
    return render(request, 'scientificWork/rads.html')


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/scientificWork/')
            else:

                return HttpResponse("Your  account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")


    else:

        return render(request, 'scientificWork/login.html', {})


# Используйте декоратор login_required(), чтобы гарантировать, что только авторизированные пользователи смогут получить доступ к этому представлению.
@login_required
def user_logout(request):
    # Поскольку мы знаем, что только вошедшие в систему пользователи имеют доступ к этому представлению, можно осуществить выход из системы
    logout(request)

    # Перенаправляем пользователя обратно на главную страницу.
    return HttpResponseRedirect('/scientificWork/')
