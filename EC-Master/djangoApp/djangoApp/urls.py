"""djangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from ec import views
import django
from django.conf.urls import url
from django.contrib import admin
from djangoApp import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^show/$', views.aspect_display),
    url(r'^api/aspect-analyse/query/$', views.get_aspect_analyse_json),
    url( r'^static/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.STATIC_FILES_DIRS }), 
]
