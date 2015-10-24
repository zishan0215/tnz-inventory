from django.conf.urls import patterns, url
from user import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^logout/', views.logout_user, name='logout'),
)
