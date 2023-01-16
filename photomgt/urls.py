"""photomgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.frontpage),
    path('index_all', views.index_all),
    path('avail_dates', views.return_avail_dates),
    re_path(r'^plist/(.+)/$', views.return_property),
    re_path(r'^day/(.+)/$', views.daypage),

    # path('create_navigate_index', views.create_navigate_index),

]