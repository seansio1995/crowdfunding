from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reports/', views.ReportListView.as_view(), name='reports'),
    url(r'report/(?P<pk>\d+)$', views.ReportListView.as_view(), name='report-list'),
]
