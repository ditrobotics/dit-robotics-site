from django.conf.urls import patterns, url

from printer_schedule import views

urlpatterns = patterns('',
    url(r'^$', views.ScheduleIndex.as_view(), name='index'),
    url(r'^archive/$', views.ScheduleArchive.as_view(), name='archive'),
    url(r'^add/$', views.ScheduleCreate.as_view(), name='create'),
    url(r'^start/(?P<pk>\d+)/$', views.ScheduleStart.as_view(), name='start'),
    url(r'^end/(?P<pk>\d+)/$', views.ScheduleEnd.as_view(), name='end'),
)
