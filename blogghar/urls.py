"""blogghar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='page_home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^simplemde/', include('simplemde.urls', namespace='simplemde')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^', include('authapp.urls', namespace='authapp')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^', include('django_private_chat.urls')),
    url(r'^discussions/', include('discussions.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^calendar/', include('happenings.urls', namespace='calendar'))
  
  

   # url(r'^', include('discussions.urls')), 
    #url('', include('social_django.urls', namespace='social')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # noqa
