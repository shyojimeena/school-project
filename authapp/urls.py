from django.conf.urls import url

from . import views

urlpatterns = [
	

    url(r'^users/', views.UsersView.as_view(), name='users'),
    url(r'^@(?P<username>[\w-]+)/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^resources/$',views.MyResourcesView.as_view(), name='my_resources'),
    url(r'^@(?P<username>[\w-]+)/comments/$', views.UserComments.as_view(), name='user_comments'),
    url(r'^(?P<username>[\w.@+-]+)/resources/$', views.UserResourcesView.as_view(), name='user_resources'),
    url(r'^accounts/profile/$', views.profile_redirector, name='user_profile'),
    url(r'^accounts/profile/update/$', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
]
