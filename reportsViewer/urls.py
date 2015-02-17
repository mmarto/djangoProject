from django.conf.urls import patterns, url
from reportsViewer import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^report/(?P<report_id>\d+)/$', views.report, name='report'),
        url(r'^request_report/$', views.request_report, name='request_report'),
        url(r'^download_report/(?P<report_id>\d+)/$', views.download_report, name='download_report'),
        url(r'^archive_report/(?P<report_id>\d+)/$', views.archive_report, name='archive_report'),
        url(r'^generate_report/$', views.generate_report, name='generate_report'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        )
