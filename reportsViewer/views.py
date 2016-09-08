from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from reportsViewer.models import Category, Report, UserReport, ReportArchive, UserReportArch
import os
import zipfile
from django.core.servers.basehttp import FileWrapper
import mimetypes
from datetime import datetime
from django.template.response import TemplateResponse
from reportsViewer.forms import RequestReportForm, PublishReportForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from reportsViewer.search import get_query
from django.db.models import Count, Sum
from django.db import connection

# Create your views here.
@login_required(login_url='/reportsViewer/login/')
def index(request):

    category_list = list()    
    context_dict = dict()
    totalReports = 0
    for category in Category.objects.order_by('name'):
        cnt = Report.objects.filter(category=category, type='P', users__id=request.user.id).count()
        totalReports += cnt
        if cnt > 0:
            category_list.append(category)
    context_dict['categories'] = category_list
    context_dict['total_reports'] = totalReports

    mostRecentReports = Report.objects.filter(type='P', users__id=request.user.id).order_by('-pub_date')[:5]
    context_dict['most_recent'] = mostRecentReports

    totals = Report.objects.filter(type='P', users__id=request.user.id).aggregate(total_size=Sum('size'), total_views=Sum('views'))
    context_dict['total_size']  = totals['total_size']
    context_dict['total_views']  = totals['total_views']

    topCategories = Category.objects.filter(report__type='P', report__users=request.user.id).values('name').annotate(total=Count('report__id')).order_by('-total')[:5]
    context_dict['top_categories'] = topCategories
    #search for report
    result_list = []
    query_string = ''
    if request.method == 'POST' or 'query' in request.GET:
        if ('query' in request.POST and request.POST['query'].strip()) or request.GET['query'].strip():
            if 'query' in request.POST:
                query_string = request.POST['query'] 
            elif 'query' in request.GET:
                query_string = request.GET['query']
            entry_query = get_query(query_string, ['title', 'path']) #['title', 'comment'] any field is searchable
            #print(Report.objects.filter(entry_query, users__id=request.user.id).order_by('-pub_date').query)
            found_entries = Report.objects.filter(entry_query, users__id=request.user.id).order_by('-pub_date')
            paginator = Paginator(found_entries, 15) 
            page = request.GET.get('page')
            try:
                found_entries = paginator.page(page)
            except PageNotAnInteger:
                found_entries = paginator.page(1)
            except EmptyPage:
                found_entries = paginator.page(paginator.num_pages)
            context_dict['query_string'] = query_string   
            context_dict['found_entries'] = found_entries   
    
    response = render(request, 'reportsViewer/index.html', context_dict)    
    
    return response

@login_required(login_url='/reportsViewer/login/')
def realtime_reports(request):
    category_list = list()
    for category in Category.objects.order_by('name'):
        cnt = Report.objects.filter(category=category, type='R', users__id=request.user.id).count()
        if cnt > 0:
            category_list.append(category)
    context_dict = {'categories': category_list}

    response = render(request, 'reportsViewer/realtime_reports.html', context_dict)
    return response

@login_required(login_url='/reportsViewer/login/')
def archive(request):
    category_list = list()
    # print(Category.objects.order_by('name').query)
    for category in Category.objects.order_by('name'):
        # print(ReportArchive.objects.filter(category=category, users__id=request.user.id).query)
        cnt = ReportArchive.objects.filter(category=category, users__id=request.user.id).count()
        if cnt > 0:
            category_list.append(category)
    context_dict = {'categories': category_list}
    query_string = ''
    if request.method == 'POST' or 'query' in request.GET:
        if ('query' in request.POST and request.POST['query'].strip()) or request.GET['query'].strip():
            if 'query' in request.POST:
                query_string = request.POST['query']
            elif 'query' in request.GET:
                query_string = request.GET['query']
            entry_query = get_query(query_string, ['title', 'path']) #['title', 'comment'] any field is searchable
            #print(Report.objects.filter(entry_query, users__id=request.user.id).order_by('-pub_date').query)
            found_entries = ReportArchive.objects.filter(entry_query, users__id=request.user.id).order_by('-pub_date')
            paginator = Paginator(found_entries, 15) 
            page = request.GET.get('page')
            try:
                found_entries = paginator.page(page)
            except PageNotAnInteger:
                found_entries = paginator.page(1)
            except EmptyPage:
                found_entries = paginator.page(paginator.num_pages)
            context_dict['query_string'] = query_string   
            context_dict['found_entries'] = found_entries   
    response = render(request, 'reportsViewer/archive.html', context_dict)
    return response


@login_required(login_url='/reportsViewer/login/')
def category(request, category_name_slug, type=None):
    print(category_name_slug,type)    
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        reports_list = Report.objects.filter(category=category, type='P', users__id=request.user.id).order_by('-pub_date')

        paginator = Paginator(reports_list, 15)

        page = request.GET.get('page')
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        
        #print(reports.count())
        #print(request.user.id)

        context_dict['reports'] = reports

        context_dict['category'] = category

    except Category.DoesNotExist:
        pass
    
    return render(request, 'reportsViewer/category.html', context_dict)

@login_required(login_url='/reportsViewer/login/')
def category_realtime(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        reports_list = Report.objects.filter(category=category, type='R', users__id=request.user.id).order_by('-pub_date')

        paginator = Paginator(reports_list, 25)

        page = request.GET.get('page')
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)

        #print(reports.count())
        #print(request.user.id)

        context_dict['reports'] = reports

        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'reportsViewer/category_realtime.html', context_dict)

@login_required(login_url='/reportsViewer/login/')
def category_archive(request, category_name_slug):
   
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        reports_list = ReportArchive.objects.filter(category=category, type='P', users__id=request.user.id).order_by('-pub_date')

        paginator = Paginator(reports_list, 25)

        page = request.GET.get('page')
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)

        #print(reports.count())
        #print(request.user.id)

        context_dict['reports'] = reports

        context_dict['category'] = category

    except Category.DoesNotExist:
        pass
   
    return render(request, 'reportsViewer/category_archive.html', context_dict)


@login_required(login_url='/reportsViewer/login/')
def report(request, report_id):

    context_dict = {}
    try:
        report = Report.objects.get(id=report_id, users__id=request.user.id)    
        #print(report.title)
        context_dict['report'] = report
    except Report.DoesNotExist:
        pass

    return render(request, 'reportsViewer/report.html', context_dict) 

@login_required(login_url='/reportsViewer/login/')
def report_realtime(request, report_id):

    context_dict = {}
    try:
        report = Report.objects.get(id=report_id, users__id=request.user.id)
        #print(report.title)
        context_dict['report'] = report
    except Report.DoesNotExist:
        pass

    return render(request, 'reportsViewer/report_realtime.html', context_dict)

@login_required(login_url='/reportsViewer/login/')
def report_archive(request, report_id):

    context_dict = {}
    try:
        report = ReportArchive.objects.get(id=report_id, users__id=request.user.id)    
        #print(report.title)
        context_dict['report'] = report
    except ReportArchive.DoesNotExist:
        pass

    return render(request, 'reportsViewer/report_archive.html', context_dict) 

@login_required(login_url='/reportsViewer/login/')
def download_report(request, report_id):
    try:
        report = Report.objects.get(id=report_id, users__id=request.user.id)
        report.views += 1
        report.save()
        filename = report.path
        chunk_size = 8192
        try:
            response = StreamingHttpResponse(FileWrapper(open(filename, 'rb'), chunk_size), content_type=mimetypes.guess_type(filename)[0]) 
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = 'attachement; filename={}'.format(os.path.basename(filename))
        except FileNotFoundError:
            return HttpResponse('Report does not exist: {}'.format(filename))
        return response
    except Report.DoesNotExist:
        pass

@login_required(login_url='/reportsViewer/login/')
def download_report_archive(request, report_id):
    try:
        report = ReportArchive.objects.get(id=report_id, users__id=request.user.id)
        report.views += 1
        report.save()
        filename = report.path
        chunk_size = 8192
        try:
            response = StreamingHttpResponse(FileWrapper(open(filename, 'rb'), chunk_size), content_type=mimetypes.guess_type(filename)[0]) 
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = 'attachement; filename={}'.format(os.path.basename(filename))
        except FileNotFoundError:
            return HttpResponse('Report does not exist: {}'.format(filename))
        return response
    except ReportArchive.DoesNotExist:
        pass

@login_required(login_url='/reportsViewer/login/')
def generate_report(request, report_id):

    report = Report.objects.get(id=report_id, users__id=request.user.id)
    head, tail = os.path.split(report.path)
    head = os.path.basename(head)
    birtReport = os.path.join('reports', os.path.join(head,tail))
    #print(birtReport)
    #html = "http://sdev100:8080/birt_new/frameset?__report=Cs_Stats_YYYYMMDD(MON).rptdesign"
    html = "http://localhost:28080/birt/frameset?__report={}".format(birtReport)
    response = TemplateResponse(request, 'reportsViewer/generate_report.html', {'message': html})

    #return HttpResponse(html)
    return response

@login_required(login_url='/reportsViewer/login/')
def archive_report(request, report_id):
    report = Report.objects.get(id=report_id, users__id=request.user.id)
    # userReportPerm = UserReport.objects.get(user_id=request.user.id, report_id=report_id)
    userReportPerms = UserReport.objects.filter(report_id=report_id)
    # print(UserReport.objects.filter(report_id=report_id).query)
    # print(report.category.slug, report.category.dir, report.category.archive_dir)    
    filename = os.path.basename(report.path)
    archivePath = '{0}/{1}'.format(report.category.archive_dir, filename)
    zipFileName = '{}.zip'.format(archivePath)
    # print(archivePath)
    os.rename(report.path, archivePath)
    zf = zipfile.ZipFile(zipFileName, mode='w')
    try:
        zf.write(archivePath)
    finally:
        zf.close()
        os.remove(archivePath)
    zipSize = os.path.getsize(zipFileName)

    archiveReport = ReportArchive(id=report.id, 
                                    title=report.title, 
                                    path=zipFileName, 
                                    views=report.views, 
                                    pub_date=report.pub_date, 
                                    creator=report.creator, 
                                    size=zipSize, 
                                    category_id=report.category_id, 
                                    type=report.type, 
                                    comment=report.comment)
    archiveReport.save()

    for userReportPerm in userReportPerms:
        archiveUserReportPerm = UserReportArch(id=userReportPerm.id, user_id=request.user.id, report_id=report_id)
        archiveUserReportPerm.save(force_insert=True)
        # print(connection.queries[-1])
        userReportPerm.delete()

    report.delete()
    return HttpResponseRedirect('/reportsViewer/category/{}'.format(report.category.slug))

@login_required(login_url='/reportsViewer/login/')
def delete_report(request, report_id):
    report = Report.objects.get(id=report_id, users__id=request.user.id)
    userReportPerm = UserReport.objects.get(user_id=request.user.id, report_id=report_id)
    userReportPerm.delete()
    return HttpResponseRedirect('/reportsViewer/category/{}'.format(report.category.slug))

@login_required(login_url='/reportsViewer/login/')
def delete_report_archive(request, report_id):
    report = ReportArchive.objects.get(id=report_id, users__id=request.user.id)
    userReportPerm = UserReportArch.objects.get(user_id=request.user.id, report_id=report_id)
    userReportPerm.delete()
    return HttpResponseRedirect('/reportsViewer/category_archive/{}'.format(report.category.slug))

def user_login(request):
    
    next = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect('/reportsViewer/')
            else:
                return HttpResponse('Your Reports Viewer account is disabled.')
        else:
            #print('Invalid login details: {}, {}'.format(username, password))
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'reportsViewer/login.html', {'next': next})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/reportsViewer/login/')

@login_required
def request_report(request):
    if request.method == 'POST':
        #form = RequestReportForm(request.POST, user=request.user)
        form = RequestReportForm(request.POST)
        form.instance.user_id = request.user.id
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        #form = RequestReportForm(user=request.user)
        form = RequestReportForm()
    return render(request, 'reportsViewer/request_report.html', {'form': form})

@login_required
def publish_report(request):
    form = PublishReportForm()
    context = {'form': form}
    template = 'reportsViewer/publish_report.html'
    return render(request, template, context)

@login_required
def publish_report_save(request):
    print('yo')
