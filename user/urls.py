from django.conf.urls import patterns, url
from user import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^new/', views.new_item, name='new_item'),
    url(r'^view/', views.view_items, name='view_items'),
    url(r'^search/', views.search, name='search'),
    url(r'^logout/', views.logout_user, name='logout'),
)
