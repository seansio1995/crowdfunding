from django.conf.urls import url
from . import views
from django.conf import settings
from django.contrib.auth.views import logout




urlpatterns = [
    url(r'^reports/', views.report_list, name='reports'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.Login, name = 'login'),
    url(r'^messaging/$', views.messaging, name = 'messaging'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^createreport/$', views.createreport, name='createreport'),
    url(r'^viewreport/(?P<pk>[0-9]+)/$', views.viewreport, name='viewreport'),
    url(r'^viewreport/(?P<pk>[0-9]+)/$', views.edit_report, name='viewreport'),
    url(r'^viewreport/(?P<pk>[0-9]+)/success/$', views.viewreport, name='viewreport'),
    url(r'^viewallreport/$', views.viewallreport, name='viewallreport'),
    url(r'^viewallreport/(?P<pk>[0-9]+)/$', views.edit_report, name='edit_report'),
    url(r'^viewallreport/(?P<pk>[0-9]+)/success/$', views.finish_edit, name='finish_edit'),
    url(r'^loggedin/$', views.user_home, name='userhome'),
    url(r'^createG/$', views.create_group, name='create-group'),
    url(r'^addGuser/$', views.add_user_to_group, name='add-user-g'),
    url(r'^userG/$', views.group_list, name='Glist'),
    url(r'^manager/$', views.manager_home, name='managerhome'),
    url(r'^addsm/$', views.add_SM, name='addSM'),
    url(r'^deleteuser/$', views.delete_user, name='delete-user-g'),
    url(r'^adderror/$', views.add_error, name='add-error'),
    url(r'^Suspend/$', views.suspend_user, name='suspend'),
    url(r'^UnSuspend/$', views.unsuspend_user, name='unsuspend'),
    url(r'^sendmessage/$',views.send_message,name="sendmessage"),
    url(r'^receivemessage/$',views.receive_message,name="receivemessage"),
    url(r'^gohome/$',views.gohome,name="gohome"),
    url(r'^mem/(?P<pk>[0-9]+)/$',views.viewgroup, name = 'members'),
    url(r'^projects/$',views.project_list, name = 'projects'),
    url(r'^allprojects/$', views.project_list_all, name='allprojects'),
    url(r'^upvote/(?P<pk>[0-9]+)/$', views.upvote_project, name='upvote'),
    url(r'^addproject/(?P<pk>[0-9]+)/$', views.add_project, name='addproject'),
    url(r'^createP/$', views.create_project, name='createproject'),
    url(r'^search/', views.search, name='search')
]
