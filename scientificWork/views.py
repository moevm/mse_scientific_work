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

    return render(request,'scientificWork/index.html')
    #return HttpResponse(o)



def competitions(request):
    return render(request,'scientificWork/competitions.html')

def publications(request):
    o = Publication.objects.all()


    if request.method == 'GET' and request.GET.items():
        if 'author' in request.GET:
            o = o.filter(user__patronymic=request.GET.get('author'))
        if 'type' in request.GET:
            o = o.filter(typePublication=request.GET.get('type'))
        if 'date' in request.GET:
            o = o.filter(date=request.GET.get('date'))


    template = loader.get_template('scientificWork/publications.html')
    context = RequestContext(request, {
        'o': o,
    })
    print_peport_publications_docx(o)
    print_list_publications_xls(o)
    return HttpResponse(template.render(context))

def staff(request):
    s = UserProfile.objects.all()

    if request.method == 'GET' and request.GET.items():
        if 'position' in request.GET:
            s = s.filter(type=request.GET.get('position'))
        if 'name' in request.GET:
            s = s.filter(patronymic=request.GET.get('name'))
        if 'degree' in request.GET:
            s = s.filter(academic_degree=request.GET.get('degree'))

    for x in s:

        x.typestr=x.get_type_display()
        x.academic_degreestr=x.get_academic_degree_display()

        x.typestr = x.get_type_display()
        x.academic_degreestr = x.get_academic_degree_display()


    template = loader.get_template('scientificWork/staff.html')
    context = RequestContext(request, {
        's': s,
    })

    print_peport_staff_docx(s)
    print_list_staff_xls(s)
    return HttpResponse(template.render(context))

def rads(request):
    return render(request,'scientificWork/rads.html')



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
