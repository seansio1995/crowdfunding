from django.conf.urls import url
from mysite.core import views as core_views

from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', core_views.signup, name='signup'),
]
