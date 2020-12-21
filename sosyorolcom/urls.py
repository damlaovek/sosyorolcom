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
    path('savenewquiz/', sv.savenewquiz, name="savenewquiz"),
    path('savenewpost/', sv.savenewpost, name="savenewpost"),
    path('savenewlink/', sv.savenewlink, name="savenewlink"),
    path('savenewpoll/', sv.savenewpoll, name="savenewpoll"),
    path('savenewquestion/', sv.savenewquestion, name="savenewquestion"),
    path('savenewmediapost/', sv.savenewmediapost, name="savenewmediapost"),
    path('savenewanswer/', sv.savenewanswer, name="savenewanswer"),
    path('savecomment/', sv.savecomment, name='savecomment'),
    path('loadmorecomments/', sv.loadmorecomments, name='loadmorecomments'),
    path('pickpostcommunities', sv.pickpostcommunities, name="pickpostcommunities"),
    path('getcommunityflairs', sv.getcommunityflairs, name="getcommunityflairs"),
    path('addanotherquizresult/', sv.addanotherquizresult, name="addanotherquizresult"),
    path('addanotherquizquestion/', sv.addanotherquizquestion, name="addanotherquizquestion"),
    path('getquizresult/', sv.getquizresult, name='getquizresult'),
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
    path('u/<path:parent_author_name>/<path:parent_post_id>/<slug:parent_slug>/answer/<path:author_name>', sv.answerdetail, name="answerdetail"),
    path('u/<path:username>/<path:post_id>/<slug:slug>', sv.postdetail, name='postdetail'),
    path('u/<path:username>/<path:post_id>/<slug:slug>/', sv.postdetail, name='postdetail'),
    path('u/<slug:username>', sv.userprofile, name='userprofile'),
    path('u/<slug:username>/followers', sv.userfollowers, name='userfollowers'),
    path('u/<slug:username>/followings', sv.userfollowings, name='userfollowings'),
    path('u/<slug:username>/suggested', sv.usersuggested, name='usersuggested'),
    path('u/<slug:username>/<path:filter>', sv.userprofile, name='userprofile'),
    path('loadmoreprofileposts', sv.loadmoreprofileposts, name='loadmoreprofileposts'),
    path('savenewusercredential', sv.savenewusercredential, name="savenewusercredential"),
    path('deleteusercredential', sv.deleteusercredential, name="deleteusercredential"),
    path('editusercredential', sv.editusercredential, name="editusercredential"),
    path('getlanguages', sv.getlanguages, name="getlanguages"),
    path('followunfollowuser', sv.followunfollowuser, name="followunfollowuser"),
    path('changeprofilepicture/', sv.changeprofilepicture, name="changeprofilepicture"),
    path('removeprofilepicture/', sv.removeprofilepicture, name="removeprofilepicture"),
    path('updatenotification', sv.updatenotification, name="updatenotification"),
    path('updateallnotifications/', sv.updateallnotifications, name="updateallnotifications"),
    path('notifications/', sv.notifications, name="notifications"),
    path('notifications/<path:filter>', sv.notifications, name="notifications"),
    path('questions', sv.questions, name='questions'),
    path('followpost', sv.followpost, name='followpost'),
    path('get_searched_users', sv.get_searched_users, name='get_searched_users'),
    path('requestanswer', sv.requestanswer, name='requestanswer'),
    path('answer/requests', sv.answerrequests, name='answerrequests'),
    path('answer/answer_later', sv.answerdrafts, name='answerdrafts'),
    path('saveanswerdraft', sv.saveanswerdraft, name='saveanswerdraft'),
    path('publishdraftanswer', sv.publishdraftanswer, name='publishdraftanswer'),
    path('deleteanswerdraft', sv.deleteanswerdraft, name='deleteanswerdraft'),
    path('quizzes', sv.quizzes, name='quizzes'),
    path('quizzes/<path:filter>', sv.quizzesfiltered, name='filteredquizzes'),
    path('quiz/requests', sv.quizrequests, name='quizrequests'),
    path('polls', sv.polls, name='polls'),
    path('polls/<path:filter>', sv.pollsfiltered, name='filteredpolls'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
