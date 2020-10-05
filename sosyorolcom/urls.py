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
    path('signup', sv.signup, name="signup"),
    path('signin', sv.signin, name="signin"),
    path('phonecodeverification', sv.phonecodeverification, name="phonecodeverification"),
    path('accounts/password/reset/', sv.resetpassword, name="resetpassword"),
    path('accounts/password/reset/verify', sv.verifyresetpassword, name="verifyresetpassword"),
    path('logout', sv.signout, name="logout"),
    path('search', sv.search, name="search"),
    path('getsearchresults', sv.get_search_results, name="get_search_results"),
    path('checkusernamevalidity', sv.checkusername, name="checkusernamevalidity"),
    path('feed/history/', sv.history, name="history"),
    path('feed/history/<path:filter>', sv.history, name="history"),
    path('feed/saved/', sv.savedposts, name="savedposts"),
    path('feed/saved/<path:post_type>', sv.savedpostsfilter, name="savedpostsfilter"),
    path('save-the-post/', sv.savethepost, name="save-the-post"),
    path('submit/', sv.newpost, name="newpost"),
    path('addanotherquizresult/', sv.addanotherquizresult, name="addanotherquizresult"),
    path('votepoll/', sv.votepoll, name='votepoll'),
    path('postrating/', sv.postrating, name='postrating'),
    path('uploadmedia/', sv.uploadmedia, name='uploadmedia'),
    path('uploadmediagetcolor/', sv.uploadmediagetcolor, name='uploadmediagetcolor'),
    path('feed/lists/', sv.lists, name='lists'),
    path('feed/lists/morefollowedlists', sv.morefollowedlists, name='morefollowedlists'),
    path('feed/lists/<slug:slug>/', sv.listdetail, name='listdetail'),
    path('communities/leaderboard/', sv.communities, name='communities'),
    path('loadmoreleaderboardcommunities', sv.morecommunities, name='loadmoreleaderboardcommunities'),
    path('communities/leaderboard/<path:filter>', sv.communitiesfiltered, name='filteredcommunities'),
    path('c/communities/create', sv.newcommunity, name='newcommunity'),
    path('c/communities/create/savenewcommunity', sv.savenewcommunity, name='savenewcommunity'),
    path('c/<slug:slug>/', sv.communitydetail, name='communitydetail'),
    path('c/<slug:slug>/<path:filter>', sv.communitydetail, name='communitydetail'),
    path('followlist', sv.follow_unfollow_list, name='followlist'),
    path('feed/lists/create', sv.createlist, name='createlist'),
    path('feed/lists/create/savenewlist/', sv.savenewlist, name='savenewlist'),
    path('feed/lists/<slug:slug>/<path:post_type>', sv.listdetailfilter, name='listdetailfilter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
