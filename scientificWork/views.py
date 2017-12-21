#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
import datetime
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from report import *
from django.core.files.storage import FileSystemStorage
from scientificWork.models import Publication, UserProfile,MediaModel


def index(request):
    return render(request, 'scientificWork/index.html')


def lk(request):
    if (request.user.is_authenticated()):
        us = request.user
        profile = UserProfile.objects.get(user=us)
        profile_d = UserProfile_d(profile)
        o = Publication.objects.all()
        if 'deleteBook' in request.GET:
            if o.filter(id=request.GET.get('deleteBook')).exists():
                c = o.filter(id=request.GET.get('deleteBook'))
                c.delete()
        o = o.filter(user=profile)
        o1 = []
        for p in o:
            o2 = Publication_d(p)
            o1 += [o2]
        template = loader.get_template('scientificWork/lk.html')
        context = RequestContext(request, {
            'profile': profile_d,
            'publications': o1,
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponse("Пожалуйста авторизуйтесь")

def editPublication(request):
    if request.user.is_authenticated():
        st = 0
        id = request.GET.get('id')
        pub = Publication.objects.get(id=id)
        pubdate=pub.date
        pubdate=datetime.date.strftime(pubdate,"%Y-%m-%d")
        if 'bookName' in request.GET:
            bookName = request.GET.get('bookName')
            typePublication = request.GET.get('type')
            date = request.GET.get('date')
            publishingHouseName = request.GET.get('publishingHouseName')
            place = request.GET.get('place')
            volume = request.GET.get('volume')
            unitVolume = request.GET.get('unitVolume')
            edition = request.GET.get('edition')
            citingBase = request.GET.get('citingBase')
            st = 1
            pub.publishingHouseName=publishingHouseName; pub.place=place; pub.date=datetime.datetime.strptime(date, "%Y-%m-%d")
            pub.volume=volume; pub.unitVolume=unitVolume; pub.edition=edition; pub.typePublication=typePublication; pub.bookName=bookName
            pub.citingBase=citingBase
            pub.save()
        template = loader.get_template('scientificWork/editPublication.html')
        context = RequestContext(request, {
            'st': st, 'pub': pub, 'id':id, 'pubdate':pubdate
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponse("Авторизуйтесь или зарегистрируйтесь")




def addPublication(request):
    if request.user.is_authenticated():
        st = 0
        if 'bookName' in request.GET:
            us = request.user
            profile = UserProfile.objects.get(user=us)
            bookName = request.GET.get('bookName')
            typePublication=request.GET.get('type')
            date=request.GET.get('date')
            publishingHouseName=request.GET.get('publishingHouseName')
            place=request.GET.get('place')
            volume=request.GET.get('volume')
            unitVolume=request.GET.get('unitVolume')
            edition=request.GET.get('edition')
            citingBase=request.GET.get('citingBase')
            st = 1
            p = Publication(user=profile, publishingHouseName=publishingHouseName, place=place,
                            date=datetime.datetime.strptime(date, "%Y-%m-%d"), volume=volume, unitVolume=unitVolume,
                            edition=edition, type="book1", typePublication=typePublication, bookName=bookName,
                            isbn="jj",
                            number=1, editor="Andy", reiteration='disposable', citingBase=citingBase)
            p.save()

        template = loader.get_template('scientificWork/addPublication.html')
        context = RequestContext(request, {
            'st': st,
        })

        return HttpResponse(template.render(context))
    else:
        return HttpResponse("Авторизуйтесь или зарегистрируйтесь")


def competitions(request):
    return render(request, 'scientificWork/competitions.html')

def registration(request):
    ctx = {}
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        birth_date=request.POST['birth_date']
        github_id = request.POST['github_id']
        stepic_id = request.POST['stepic_id']
        type = request.POST['type']
        position = request.POST['position']
        election_date = request.POST['election_date']
        contract_date = request.POST['contract_date']
        academic_degree = request.POST['academic_degree']
        year_of_academic_degree = request.POST['year_of_academic_degree']
        academic_status = request.POST['academic_status']
        year_of_academic_status = request.POST['year_of_academic_status']
        user = User.objects.create_user(username=username, password = password)
        user.is_superuser=False
        user.is_staff=False
        user.save()
        profile=UserProfile(user=user,patronymic=username,birth_date=datetime.datetime.strptime(birth_date, "%Y-%m-%d"),study_group="1",
                            github_id=github_id,stepic_id=stepic_id,type=type,election_date=datetime.datetime.strptime(election_date, "%Y-%m-%d"),position=position,
                            contract_date=datetime.datetime.strptime(contract_date, "%Y-%m-%d"),academic_degree=academic_degree,year_of_academic_degree=datetime.datetime.strptime(year_of_academic_degree, "%Y-%m-%d"),
                            academic_status=academic_status,year_of_academic_status=datetime.datetime.strptime(year_of_academic_status, "%Y-%m-%d"),
                            user_role='u')
        profile.save()
        ctx.update(csrf(request))
        ctx['st'] = 1
        ctx['username'] = request.POST['username']
        return render(request, "scientificWork/registration.html", ctx)
    else:
        ctx['st'] = 0
        return render(request, 'scientificWork/registration.html', ctx)

def publications(request):
    o = Publication.objects.all()
    filters = []
    f = MediaModel.objects.all()
    if 'deleteFile' in request.GET:
        if f.filter(id=request.GET.get('deleteFile')).exists():
            z=f.filter(id=request.GET.get('deleteFile'))
            z.delete()
    if 'deleteBook' in request.GET:
        if o.filter(id=request.GET.get('deleteBook')).exists():
            c = o.filter(id=request.GET.get('deleteBook'))
            c.delete()
    if request.method == 'GET' and request.GET.items():
        if 'bookName' in request.GET:
            if len(request.GET.get('bookName')) > 0:
                o = o.filter(bookName=request.GET.get('bookName'))
                if o.filter(bookName=request.GET.get('bookName')).exists(): filters += ['bookName']
        if 'author' in request.GET:
            author_name = request.GET.get('author')
            if UserProfile.objects.filter(patronymic=author_name).exists():
                author = UserProfile.objects.get(patronymic=author_name)
                o = o.filter(user=author)
                filters += ['author']
            elif len(author_name) > 0:
                o = o.filter(user=None)
        if 'type' in request.GET:
            if request.GET.get('type') != "all":
                o = o.filter(typePublication=request.GET.get('type'))
                if o.filter(typePublication=request.GET.get('type')).exists(): filters += ['type']
        if 'date' in request.GET:
            try:
                if len(request.GET.get('date')) > 0:
                    o = o.filter(date=request.GET.get('date'))
                    if o.filter(date=request.GET.get('date')).exists(): filters += ['date']
            except(ValidationError):
                o = o.filter(date=None)
        if 'citing' in request.GET:
            o = o.filter(citingBase=request.GET.get('citing'))

    o1 = []
    for p in o:
        o2 = Publication_d(p)
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
        if 'deleteProfile' in request.GET:
            if s.filter(id=request.GET.get('deleteProfile')).exists():
                c = s.get(id=request.GET.get('deleteProfile'))
                user=c.user
                #users=User.objects.all()
                #prof=users.filter()
                c.delete()
                user.delete()
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
                if s.filter(patronymic=request.GET.get('name')).exists(): filters += ["name"]
        if 'contract_date' in request.GET:
            try:
                if len(request.GET.get('contract_date')) > 0:
                    s = s.filter(contract_date=request.GET.get('contract_date'))
                    filters += ["contract_date"]
            except(ValidationError):
                s = s.filter(contract_date=None)
        if 'academic_status' in request.GET:
            if request.GET.get('academic_status') != "all":
                s = s.filter(academic_status=request.GET.get('academic_status'))
                filters += ["academic_status"]
    s1 = []
    for x in s:
        s2 = UserProfile_d(x)
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

        username = request.POST.get('username').encode('utf8')
        password = request.POST.get('password').encode('utf8')

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


def UserProfile_d(x):
    s2 = {}
    s2["id"] = x.id
    s2["type"] = x.get_type_display()
    s2["academic_degree"] = x.get_academic_degree_display()
    s2["name"] = x.patronymic
    s2["contract_date"] = datetime.date.strftime(x.contract_date,"%Y-%m-%d")
    s2["academic_status"] = x.get_academic_status_display()
    return s2


def Publication_d(p):
    o2 = {}
    o2["id"] = p.id
    o2["bookName"] = p.bookName
    o2["author"] = p.user.patronymic
    o2["date"] = datetime.date.strftime(p.date,"%Y-%m-%d")
    o2["type"] = p.get_typePublication_display()
    f=MediaModel.objects.all()
    f1=f.filter(owner=p)
    o2["f"]=f1
    return o2


def upload_file(request):

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        M=MediaModel(media_file=myfile,owner=Publication.objects.get(id=request.GET.get("pub")))
        M.save()
        m = MediaModel.objects.all()
        return render(request, 'scientificWork/upload_file.html', { 'pub': 0})
    m = MediaModel.objects.all()
    pub=request.GET.get("pub")
    return render(request, 'scientificWork/upload_file.html', {'pubname':Publication.objects.get(id=request.GET.get("pub")).bookName, 'pub': pub})
