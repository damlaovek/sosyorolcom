"""sosyorolcom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
import sosyorol.views as sv
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('', sv.home),
    path('saved/', sv.savedposts, name="savedposts"),
    path('saved/<path:post_type>', sv.savedpostsfilter, name="savedpostsfilter"),
    path('save-the-post/', sv.savethepost, name="save-the-post"),
    path('submit/', sv.newpost),
    path('votepoll/', sv.votepoll, name='votepoll'),
    path('postrating/', sv.postrating, name='postrating'),
    path('uploadmedia/', sv.uploadmedia, name='uploadmedia'),
    path('uploadmediagetcolor/', sv.uploadmediagetcolor, name='uploadmediagetcolor'),
    path('c/<slug:slug>/', sv.communitydetail, name='communitydetail'),
    path('c/lists/', sv.lists, name='lists'),
    path('c/lists/morefollowedlists', sv.morefollowedlists, name='morefollowedlists'),
    path('followlist', sv.follow_unfollow_list, name='followlist'),
    path('c/lists/create', sv.createlist, name='createlist'),
    path('c/lists/create/savenewlist/', sv.savenewlist, name='savenewlist'),
    path('c/lists/<slug:slug>/', sv.listdetail, name='listdetail'),
    path('c/lists/<slug:slug>/<path:post_type>', sv.listdetailfilter, name='listdetailfilter'),
    path('c/communities/create', sv.newcommunity, name='newcommunity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
