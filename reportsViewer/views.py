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
from reportsViewer.forms import RequestReportForm

# Create your views here.
@login_required(login_url='/reportsViewer/login/')
def index(request):
    #get cookie visits
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    category_list = list()    
    for category in Category.objects.order_by('name'):
        cnt = Report.objects.filter(category=category, users__id=request.user.id).count()
        if cnt > 0:
            category_list.append(category)
    context_dict = {'categories': category_list}
    
    response = render(request, 'reportsViewer/index.html', context_dict)
    
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True


    if reset_last_visit_time:
        if hasattr(request,'session'):
            None
            #response.session['last_visit'] = datetime.now()
            #response.session['visits'] = visits
    
    context_dict['visits'] = visits
    response = render(request, 'reportsViewer/index.html', context_dict)    
    
    return response

@login_required(login_url='/reportsViewer/login/')
def category(request, category_name_slug):
    
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        reports = Report.objects.filter(category=category, users__id=request.user.id)

        #print(reports.count())
        #print(request.user.id)

        context_dict['reports'] = reports

        context_dict['category'] = category

    except Category.DoesNotExist:
        pass
    
    return render(request, 'reportsViewer/category.html', context_dict)

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
def download_report(request, report_id):
    try:
        report = Report.objects.get(id=report_id, users__id=request.user.id)
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
def generate_report(request):
    
    html = "http://sdev100:8080/birt_new/frameset?__report=Cs_Stats_YYYYMMDD(MON).rptdesign"
    response = TemplateResponse(request, 'reportsViewer/generate_report.html', {'message': html})

    #return HttpResponse(html)
    return response

@login_required(login_url='/reportsViewer/login/')
def archive_report(request, report_id):
    report = Report.objects.get(id=report_id, users__id=request.user.id)
    userReportPerm = UserReport.objects.get(user_id=request.user.id, report_id=report_id)
    #print(report.category.slug, report.category.dir, report.category.archive_dir)    
    filename = os.path.basename(report.path)
    archivePath = '{0}/{1}'.format(report.category.archive_dir, filename)
    zipFileName = '{}.zip'.format(archivePath)
    os.rename(report.path, archivePath)
    zf = zipfile.ZipFile(zipFileName, mode='w')
    try:
        zf.write(archivePath)
    finally:
        zf.close()
        os.remove(archivePath)
    
    archiveReport = ReportArchive(id=report.id, 
                                    title=report.title, 
                                    path=zipFileName, 
                                    views=report.views, 
                                    pub_date=report.pub_date, 
                                    creator=report.creator, 
                                    size=report.size, 
                                    category_id=report.category_id, 
                                    type=report.type, 
                                    comment=report.comment)
    archiveUserReportPerm = UserReportArch(id=userReportPerm.id, user_id=request.user.id, report_id=report_id)
    
    archiveReport.save()
    archiveUserReportPerm.save()
    
    report.delete()
    userReportPerm.delete()

    return HttpResponseRedirect('/reportsViewer/category/{}'.format(report.category.slug))

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/reportsViewer/')
            else:
                return HttpResponse('Your Reports Viewer account is disabled.')
        else:
            print('Invalid login details: {}, {}'.format(username, password))
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'reportsViewer/login.html', {})

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
