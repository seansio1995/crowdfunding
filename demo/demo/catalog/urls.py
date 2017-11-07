from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    url(r'^reports/', views.report_list, name='reports'),
    url(r'report/(?P<pk>\d+)$', views.report_list, name='report-list'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.Login, name = 'login'),
    url(r'^messaging/$', views.messaging, name = 'messaging'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^createreport/$', views.createreport, name='createreport'),
    url(r'^messaging/$', views.messaging, name='message'),
    url(r'^loggedin/$', views.loggedin, name='userhome'),
]
