from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.frontpage),
    path('index_all', views.index_all),
    path('avail_dates', views.return_avail_dates),
    re_path(r'^plist/(.+)/$', views.return_property),
    re_path(r'^day/(.+)/$', views.daypage),

    # path('create_navigate_index', views.create_navigate_index),

]