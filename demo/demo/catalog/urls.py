from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^reports/', views.report_list, name='reports'),
    url(r'report/(?P<pk>\d+)$', views.report_list, name='report-list'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.Login, name = 'login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^messaging/$', views.messaging, name='messaging'),
    url(r'^createreport/$', views.createreport, name='createreport'),
]
