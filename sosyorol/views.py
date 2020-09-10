from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from sosyorol.models import *
from sosyorol.forms import *
from django.db.models import Q
import os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup as BSHTML
import datetime as dt
import re
from urllib.request import urlopen
import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import time
from colorthief import ColorThief
from PIL import Image
import requests
import sosyorol.functions as fun
#import pyrebase
import firebase_admin
from firebase_admin import auth, credentials, exceptions
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')

'''---------------------------------------
  FIREBASE              
-----------------------------------------'''
if not firebase_admin._apps:
    cred = credentials.Certificate('static/sosyorol-b6ab6-firebase-adminsdk-q80t3-54150f4057.json') 
    default_app = firebase_admin.initialize_app(cred)
    auth = default_app.auth()

'''---------------------------------------
  DICTIONARIES              
-----------------------------------------'''
def header(word_list):
    header_dict = {}
    home = word_list.filter(Q(var_name = 'home'))[0].translation.upper()
    quizzes = word_list.filter(Q(var_name = 'quizzes'))[0].translation.upper()
    questions = word_list.filter(Q(var_name = 'questions'))[0].translation.upper()
    polls = word_list.filter(Q(var_name = 'polls'))[0].translation.upper()
    communities = word_list.filter(Q(var_name = 'communities'))[0].translation.upper()
    settings = fun.ucfirst(word_list.filter(Q(var_name = 'settings'))[0].translation)
    profile = fun.ucfirst(word_list.filter(Q(var_name = 'profile'))[0].translation)
    messages = fun.ucfirst(word_list.filter(Q(var_name = 'messages'))[0].translation)
    search = fun.ucfirst(word_list.filter(Q(var_name = 'search'))[0].translation)
    notifications = fun.ucfirst(word_list.filter(Q(var_name = 'notifications'))[0].translation)
    header_dict['createpost'] = fun.ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    header_dict['home'] = home
    header_dict['quizzes'] = quizzes
    header_dict['questions'] = questions
    header_dict['polls'] = polls
    header_dict['communities'] = communities
    header_dict['settings'] = settings
    header_dict['profile'] = profile
    header_dict['messages'] = messages
    header_dict['search'] = search
    header_dict['notifications'] = notifications
    return header_dict

def left_menu(word_list):
    left_menu_dict = {}
    left_menu_dict['createpost'] = fun.ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    left_menu_dict['feed'] = fun.ucfirst(word_list.filter(Q(var_name = 'feed'))[0].translation)
    left_menu_dict['darkmode'] = fun.ucfirst(word_list.filter(Q(var_name = 'dark-mode'))[0].translation)
    left_menu_dict['lightmode'] = fun.ucfirst(word_list.filter(Q(var_name = 'light-mode'))[0].translation)
    left_menu_dict['country'] = fun.ucfirst(word_list.filter(Q(var_name = 'lang'))[0].translation)
    left_menu_dict['about'] = fun.ucfirst(word_list.filter(Q(var_name = 'about'))[0].translation)
    left_menu_dict['careers'] = fun.ucfirst(word_list.filter(Q(var_name = 'careers'))[0].translation)
    left_menu_dict['advertise'] = fun.ucfirst(word_list.filter(Q(var_name = 'advertise'))[0].translation)
    left_menu_dict['helpvar'] = fun.ucfirst(word_list.filter(Q(var_name = 'help'))[0].translation)
    left_menu_dict['termsvar'] = fun.ucfirst(word_list.filter(Q(var_name = 'terms'))[0].translation)
    left_menu_dict['createlist'] = fun.ucwords(word_list.filter(Q(var_name = 'create-list'))[0].translation)
    left_menu_dict['lists'] = fun.ucfirst(word_list.filter(Q(var_name = 'lists'))[0].translation)
    left_menu_dict['visithistory'] = fun.ucfirst(word_list.filter(Q(var_name = 'visithistory'))[0].translation)
    left_menu_dict['savedposts'] = fun.ucfirst(word_list.filter(Q(var_name = 'savedposts'))[0].translation)
    left_menu_dict['more'] = fun.ucfirst(word_list.filter(Q(var_name = 'more'))[0].translation)
    left_menu_dict['less'] = fun.ucfirst(word_list.filter(Q(var_name = 'less'))[0].translation)
    left_menu_dict['createcommunity'] = fun.ucwords(word_list.filter(Q(var_name = 'create-community'))[0].translation)
    return left_menu_dict

def lists_achive(word_list):
    lists_dict = {}
    lists_dict['lists'] = fun.ucfirst(word_list.filter(Q(var_name = 'lists'))[0].translation)
    lists_dict['listsPageDesc'] = fun.ucfirst(word_list.filter(Q(var_name = 'lists_page_desc'))[0].translation)
    lists_dict['createList'] = fun.ucwords(word_list.filter(Q(var_name = 'create-list'))[0].translation)
    lists_dict['followLists'] = fun.ucwords(word_list.filter(Q(var_name = 'follow-lists'))[0].translation)
    lists_dict['yourlists'] = fun.ucwords(word_list.filter(Q(var_name = 'your-lists'))[0].translation)
    lists_dict['all'] = fun.ucfirst(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    lists_dict['createdbyyou'] = fun.ucfirst(word_list.filter(Q(var_name = 'created-by-you'))[0].translation)
    lists_dict['addlist'] = fun.ucwords(word_list.filter(Q(var_name = 'add-list'))[0].translation)
    lists_dict['listsyoumaylike'] = fun.ucwords(word_list.filter(Q(var_name = 'lists-you-may-like'))[0].translation)
    lists_dict['listsyoumaylikeinfo'] = fun.ucfirst(word_list.filter(Q(var_name = 'lists-you-may-like-info'))[0].translation)
    lists_dict['featured'] = fun.ucwords(word_list.filter(Q(var_name = 'featured'))[0].translation)
    lists_dict['post'] = fun.ucfirst(word_list.filter(Q(var_name = 'post'))[0].translation)
    lists_dict['members'] = fun.ucfirst(word_list.filter(Q(var_name = 'members'))[0].translation)
    lists_dict['followers'] = fun.ucfirst(word_list.filter(Q(var_name = 'followers'))[0].translation)
    lists_dict['follow'] = fun.ucfirst(word_list.filter(Q(var_name = 'follow'))[0].translation)
    lists_dict['following'] = fun.ucwords(word_list.filter(Q(var_name = 'following'))[0].translation)
    lists_dict['editlist'] = fun.ucwords(word_list.filter(Q(var_name = 'edit-list'))[0].translation)
    return lists_dict

def list_info(word_list):
    list_info_dict = {}
    list_info_dict["aboutlist"] = fun.ucwords(word_list.filter(Q(var_name = 'about-list'))[0].translation)
    list_info_dict["datecreated"] = fun.ucwords(word_list.filter(Q(var_name = 'date-created'))[0].translation)
    list_info_dict["createdby"] = fun.ucwords(word_list.filter(Q(var_name = 'created_by'))[0].translation)
    return list_info_dict

def right_menu(word_list):
    right_menu_dict = {}
    right_menu_dict['interaction'] = fun.ucwords(word_list.filter(Q(var_name = 'interaction'))[0].translation)
    right_menu_dict['scrolltotop'] = fun.localized_upper(word_list.filter(Q(var_name = 'scroll-to-top'))[0].translation)
    right_menu_dict['viewprofile'] = fun.ucwords(word_list.filter(Q(var_name = 'go-to-profile'))[0].translation)
    right_menu_dict['myprofile'] = fun.ucwords(word_list.filter(Q(var_name = 'my-profile'))[0].translation)
    right_menu_dict['createpost'] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    right_menu_dict['seeall'] = fun.ucwords(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    right_menu_dict['popularcommunities'] = fun.ucwords(word_list.filter(Q(var_name = 'popular-communities'))[0].translation)
    right_menu_dict['subscribe'] = fun.ucwords(word_list.filter(Q(var_name = 'subscribe'))[0].translation)
    right_menu_dict['trendsofcountrytitle'] = fun.ucfirst(word_list.filter(Q(var_name = 'trends-of-country-title'))[0].translation)
    right_menu_dict['showmore'] = fun.ucfirst(word_list.filter(Q(var_name = 'show-more'))[0].translation)
    right_menu_dict['usersyoumayfollow'] = fun.ucfirst(word_list.filter(Q(var_name = 'users-you-may-follow'))[0].translation)
    right_menu_dict['follow'] = fun.ucfirst(word_list.filter(Q(var_name = 'follow'))[0].translation)
    right_menu_dict['createcommunity'] = fun.ucfirst(word_list.filter(Q(var_name = 'create-community'))[0].translation)
    return right_menu_dict

def feed(word_list):
    feed_dict = {}
    feed_dict['createpost'] = fun.ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    feed_dict['trend'] = fun.ucwords(word_list.filter(Q(var_name = 'trends'))[0].translation)
    feed_dict['new'] = fun.ucwords(word_list.filter(Q(var_name = 'new'))[0].translation)
    feed_dict['contra'] = fun.ucwords(word_list.filter(Q(var_name = 'controversial'))[0].translation)
    feed_dict['rising'] = fun.ucwords(word_list.filter(Q(var_name = 'rising'))[0].translation)
    feed_dict['best'] = fun.ucwords(word_list.filter(Q(var_name = 'best'))[0].translation)
    feed_dict['now'] = fun.ucwords(word_list.filter(Q(var_name = 'now'))[0].translation)
    feed_dict['today'] = fun.ucwords(word_list.filter(Q(var_name = 'today'))[0].translation)
    feed_dict['thisweek'] = fun.ucwords(word_list.filter(Q(var_name = 'this-week'))[0].translation)
    feed_dict['thismonth'] = fun.ucwords(word_list.filter(Q(var_name = 'this-month'))[0].translation)
    feed_dict['thisyear'] = fun.ucwords(word_list.filter(Q(var_name = 'this-year'))[0].translation)
    feed_dict['alltime'] = fun.ucwords(word_list.filter(Q(var_name = 'all-time'))[0].translation)
    feed_dict['answerthequestions'] = fun.ucwords(word_list.filter(Q(var_name = 'all-time'))[0].translation)
    feed_dict['discovernewtopics'] = fun.ucwords(word_list.filter(Q(var_name = 'discover-more-communities'))[0].translation)
    feed_dict['morem'] = fun.ucwords(word_list.filter(Q(var_name = 'more'))[0].translation)
    feed_dict['followmoreusers'] = fun.ucwords(word_list.filter(Q(var_name = 'follow-more-users'))[0].translation)
    feed_dict['hiddentakeback'] = fun.ucwords(word_list.filter(Q(var_name = 'hidden-take-back'))[0].translation)
    feed_dict['hiddenusers'] = fun.ucwords(word_list.filter(Q(var_name = 'hidden-users'))[0].translation)
    feed_dict['media'] = fun.ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    feed_dict['link'] = fun.ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    feed_dict['quiz'] = fun.ucwords(word_list.filter(Q(var_name = 'quiz'))[0].translation)
    feed_dict['poll'] = fun.ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    feed_dict['question'] = fun.ucwords(word_list.filter(Q(var_name = 'question'))[0].translation)
    feed_dict['answerthequestions'] = fun.ucwords(word_list.filter(Q(var_name = 'answer-the-questions'))[0].translation)
    feed_dict['discoverthenewtopics'] = fun.ucwords(word_list.filter(Q(var_name = 'discover-more-communities'))[0].translation)
    feed_dict['followmoreusers'] = fun.ucwords(word_list.filter(Q(var_name = 'follow-more-users'))[0].translation)
    feed_dict['follow'] = fun.ucwords(word_list.filter(Q(var_name = 'follow'))[0].translation)
    return feed_dict

def new_community_tips(word_list):
    tips_dict = {}
    tips_dict["1"] = word_list.filter(Q(var_name = 'create-community-tip1'))[0].translation
    tips_dict["2"] = word_list.filter(Q(var_name = 'create-community-tip2'))[0].translation
    tips_dict["3"] = word_list.filter(Q(var_name = 'create-community-tip3'))[0].translation
    tips_dict["4"] = word_list.filter(Q(var_name = 'create-community-tip4'))[0].translation
    tips_dict["5"] = word_list.filter(Q(var_name = 'create-community-tip5'))[0].translation
    tips_dict["6"] = word_list.filter(Q(var_name = 'create-community-tip6'))[0].translation
    tips_dict["7"] = word_list.filter(Q(var_name = 'create-community-tip7'))[0].translation
    return tips_dict

def post_template(word_list):
    post_template_dict = {}
    post_template_dict['article'] = fun.ucwords(word_list.filter(Q(var_name = 'article'))[0].translation)
    post_template_dict['media'] = fun.ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    post_template_dict['link'] = fun.ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    post_template_dict['answer'] = fun.ucwords(word_list.filter(Q(var_name = 'answer'))[0].translation)
    post_template_dict['poll'] = fun.ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    post_template_dict['answernoun'] = fun.ucwords(word_list.filter(Q(var_name = 'answer-noun'))[0].translation)
    post_template_dict['recommendedfy'] = fun.ucwords(word_list.filter(Q(var_name = 'recommended-for-you'))[0].translation)
    post_template_dict['more'] = fun.ucwords(word_list.filter(Q(var_name = 'more'))[0].translation)
    post_template_dict['share'] = fun.ucwords(word_list.filter(Q(var_name = 'share'))[0].translation)
    post_template_dict['comments'] = fun.ucwords(word_list.filter(Q(var_name = 'comments'))[0].translation)
    post_template_dict['repost'] = fun.ucwords(word_list.filter(Q(var_name = 'repost'))[0].translation)
    post_template_dict['upvote'] = fun.ucwords(word_list.filter(Q(var_name = 'upvote'))[0].translation)
    post_template_dict['downvote'] = fun.ucwords(word_list.filter(Q(var_name = 'downvote'))[0].translation)
    post_template_dict['send'] = fun.ucwords(word_list.filter(Q(var_name = 'send'))[0].translation)
    post_template_dict['subscribe'] = fun.ucwords(word_list.filter(Q(var_name = 'subscribe'))[0].translation)
    post_template_dict['vote'] = fun.ucwords(word_list.filter(Q(var_name = 'vote'))[0].translation)
    post_template_dict['votenoun'] = fun.localized_lower(word_list.filter(Q(var_name = 'vote-noun'))[0].translation)
    post_template_dict['votesnoun'] = fun.localized_lower(word_list.filter(Q(var_name = 'votes-noun'))[0].translation)
    return post_template_dict

def comment_editor_dict(word_list):
    comment_editor = {}
    comment_editor['addcomment'] = fun.ucfirst(word_list.filter(Q(var_name = 'add-comment'))[0].translation)
    comment_editor['send'] = fun.ucwords(word_list.filter(Q(var_name = 'send'))[0].translation)
    return comment_editor

def post_types(word_list):
    post_types_dict = {}
    post_types_dict['post'] = fun.ucwords(word_list.filter(Q(var_name = 'post'))[0].translation)
    post_types_dict['media'] = fun.ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    post_types_dict['link'] = fun.ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    post_types_dict['quiz'] = fun.ucwords(word_list.filter(Q(var_name = 'quiz'))[0].translation)
    post_types_dict['poll'] = fun.ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    post_types_dict['question'] = fun.ucwords(word_list.filter(Q(var_name = 'question'))[0].translation)
    post_types_dict['answer'] = fun.ucwords(word_list.filter(Q(var_name = 'answer-noun'))[0].translation)
    return post_types_dict

def create_post_rules(word_list):
    create_post_rules_dict = {}
    create_post_rules_dict["1"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule1'))[0].translation)
    create_post_rules_dict["2"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule2'))[0].translation)
    create_post_rules_dict["3"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule3'))[0].translation)
    create_post_rules_dict["4"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule4'))[0].translation)
    create_post_rules_dict["5"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule5'))[0].translation)
    create_post_rules_dict["6"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule6'))[0].translation)
    create_post_rules_dict["7"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule7'))[0].translation)
    create_post_rules_dict["8"] = fun.ucfirst(word_list.filter(Q(var_name = 'create-post-rule8'))[0].translation)
    return create_post_rules_dict

def create_poll(word_list):
    create_poll_dict = {}
    create_poll_dict["createpoll"] = fun.ucwords(word_list.filter(Q(var_name = 'create-poll'))[0].translation)
    create_poll_dict["option"] = fun.ucwords(word_list.filter(Q(var_name = 'option'))[0].translation)
    create_poll_dict["pollduration"] = fun.ucwords(word_list.filter(Q(var_name = 'poll-duration'))[0].translation)
    create_poll_dict["unlimitedtime"] = fun.ucwords(word_list.filter(Q(var_name = 'unlimited-time'))[0].translation)
    create_poll_dict["day"] = fun.localized_lower(word_list.filter(Q(var_name = 'day'))[0].translation)
    create_poll_dict["days"] = fun.localized_lower(word_list.filter(Q(var_name = 'days'))[0].translation)
    create_poll_dict["addrule"] = fun.ucfirst(word_list.filter(Q(var_name = 'poll-option-add-rule'))[0].translation)
    create_poll_dict["removerule"] = fun.ucfirst(word_list.filter(Q(var_name = 'poll-option-remove-rule'))[0].translation)
    return create_poll_dict

def newpost_actions(word_list):
    newpost_actions_dict = {}
    newpost_actions_dict["title"] = fun.ucwords(word_list.filter(Q(var_name = 'title'))[0].translation)
    newpost_actions_dict['send'] = fun.ucwords(word_list.filter(Q(var_name = 'send'))[0].translation)
    newpost_actions_dict['cancel'] = fun.ucwords(word_list.filter(Q(var_name = 'cancel'))[0].translation)
    newpost_actions_dict['save'] = fun.ucwords(word_list.filter(Q(var_name = 'save'))[0].translation)
    newpost_actions_dict['clear'] = fun.ucwords(word_list.filter(Q(var_name = 'clear'))[0].translation)
    newpost_actions_dict['drafts'] = fun.ucwords(word_list.filter(Q(var_name = 'drafts'))[0].translation)
    newpost_actions_dict['searchcommunity'] = fun.ucwords(word_list.filter(Q(var_name = 'search-community'))[0].translation)
    newpost_actions_dict['spoiler'] = fun.ucfirst(word_list.filter(Q(var_name = 'spoiler-flair'))[0].translation)
    newpost_actions_dict['nsfw'] = fun.ucfirst(word_list.filter(Q(var_name = 'nsfw-flair'))[0].translation)
    newpost_actions_dict['close'] = fun.ucfirst(word_list.filter(Q(var_name = 'close'))[0].translation)
    newpost_actions_dict['delete'] = fun.ucfirst(word_list.filter(Q(var_name = 'delete'))[0].translation)
    newpost_actions_dict['lastupdated'] = fun.ucfirst(word_list.filter(Q(var_name = 'last-updated'))[0].translation)
    return newpost_actions_dict

def create_community(word_list):
    create_community_dict = {}
    create_community_dict["public"] = fun.ucwords(word_list.filter(Q(var_name = 'public'))[0].translation)
    create_community_dict["restricted"] = fun.ucwords(word_list.filter(Q(var_name = 'restricted'))[0].translation)
    create_community_dict["private"] = fun.ucwords(word_list.filter(Q(var_name = 'private'))[0].translation)
    create_community_dict["public_info_community"] = fun.ucfirst(word_list.filter(Q(var_name = 'public-info-community'))[0].translation)
    create_community_dict["restricted_info_community"] = fun.ucfirst(word_list.filter(Q(var_name = 'restricted-info-community'))[0].translation)
    create_community_dict["private_info_community"] = fun.ucfirst(word_list.filter(Q(var_name = 'private-info-community'))[0].translation)
    create_community_dict["title"] = fun.ucfirst(word_list.filter(Q(var_name = 'community-name'))[0].translation)
    create_community_dict["title_placeholder"] = fun.ucwords(word_list.filter(Q(var_name = 'community_title_placeholder'))[0].translation)
    create_community_dict["desc_placeholder"] = fun.ucfirst(word_list.filter(Q(var_name = 'community_desc_placeholder'))[0].translation)
    create_community_dict["description"] = fun.ucwords(word_list.filter(Q(var_name = 'description'))[0].translation)
    create_community_dict['cancel'] = fun.ucwords(word_list.filter(Q(var_name = 'cancel'))[0].translation)
    create_community_dict['save'] = fun.ucwords(word_list.filter(Q(var_name = 'save'))[0].translation)
    create_community_dict['clear'] = fun.ucwords(word_list.filter(Q(var_name = 'clear'))[0].translation)
    create_community_dict['nsfw'] = fun.ucfirst(word_list.filter(Q(var_name = 'nsfw-flair'))[0].translation)
    create_community_dict['edit'] = fun.ucfirst(word_list.filter(Q(var_name = 'edit'))[0].translation)
    create_community_dict['selectaprimarycategory'] = fun.ucfirst(word_list.filter(Q(var_name = 'select-a-primary-category'))[0].translation)
    create_community_dict['primarycategory'] = fun.ucfirst(word_list.filter(Q(var_name = 'primary-category'))[0].translation)
    create_community_dict['subcategoryinfo'] = word_list.filter(Q(var_name = 'subcategory-info'))[0].translation
    create_community_dict['cannotaddmorecategoryalert'] = word_list.filter(Q(var_name = 'cannot-add-more-category-alert'))[0].translation
    create_community_dict['remove'] = fun.ucfirst(word_list.filter(Q(var_name = 'remove'))[0].translation)
    create_community_dict['picturehaschanged'] = fun.ucfirst(word_list.filter(Q(var_name = 'picture-has-changed'))[0].translation)
    create_community_dict['coverpicturehaschanged'] = fun.ucfirst(word_list.filter(Q(var_name = 'cover-picture-has-changed'))[0].translation)
    create_community_dict['formerrormsg'] = fun.ucfirst(word_list.filter(Q(var_name = 'form-error-msg'))[0].translation)
    return create_community_dict

def communitydetail_dict(word_list, community_rank, followings):
    page_dict = {}
    page_dict['views'] = fun.ucfirst(word_list.filter(Q(var_name = 'views'))[0].translation)
    page_dict['usersfollowing'] = fun.ucfirst(word_list.filter(Q(var_name = 'users-are-following-this'))[0].translation)
    rank = word_list.filter(Q(var_name = 'community-rank-info'))[0].translation
    rank = rank.replace("[number]",f"<span class='fwbold'>{community_rank}</span>")
    page_dict['rank'] = rank
    page_dict['join'] = fun.ucfirst(word_list.filter(Q(var_name = 'join'))[0].translation)
    page_dict['moderators'] = fun.ucfirst(word_list.filter(Q(var_name = 'moderators'))[0].translation)
    page_dict['showmore'] = fun.ucfirst(word_list.filter(Q(var_name = 'show-more'))[0].translation)
    page_dict['filterbylabel'] = fun.ucfirst(word_list.filter(Q(var_name = 'filter-by-label'))[0].translation)
    page_dict['communityrules'] = fun.ucfirst(word_list.filter(Q(var_name = 'community-rules'))[0].translation)
    if (len(followings) == 0):
        followingsinfo = ""
    elif (len(followings) >= 3):
        followingsinfo = word_list.filter(Q(var_name = 'community-followers-info'))[0].translation
        followingsinfo = followingsinfo.replace("[number]", f"{len(followings)}")
    else:
        followingsinfo = word_list.filter(Q(var_name = 'community-followers-info2'))[0].translation
        str1 = f"<a href='/u/{followings[0].following.user_nicename}' target='_blank' class='fs13 cg2 lh30 underline-on-hover'>u/{followings[0].following.user_nicename}</a>"
        if (len(followings) == 1):
            followingsinfo = followingsinfo.replace("[user] & [user]", str1)
        else:
            str2 = f"<a href='/u/{followings[0].following.user_nicename}' target='_blank' class='fs13 cg2 lh30 underline-on-hover'>u/{followings[1].following.user_nicename}</a>"
            followingsinfo = followingsinfo.replace("[user] & [user]", f"{str1} & {str2}")
    page_dict['followingsinfo'] = followingsinfo
    return page_dict

def sign_dictionary(word_list):
    page_dict = {}
    page_dict["slogan"] = word_list.filter(Q(var_name = 'sosyorol-slogan'))[0].translation
    page_dict["createcommunity"] = fun.ucwords(word_list.filter(Q(var_name = 'create-community'))[0].translation)
    page_dict["createad"] = fun.ucwords(word_list.filter(Q(var_name = 'create-ad'))[0].translation)
    page_dict["signin"] = fun.ucfirst(word_list.filter(Q(var_name = 'signin'))[0].translation)
    page_dict["signup"] = fun.ucfirst(word_list.filter(Q(var_name = 'signup'))[0].translation)
    page_dict["forgottenpass"] = fun.ucfirst(word_list.filter(Q(var_name = 'forgotten-pass'))[0].translation)
    page_dict["sosyorolinfo"] = fun.ucfirst(word_list.filter(Q(var_name = 'sosyorol-info'))[0].translation)
    page_dict["dontyouhaveanaccount"] = fun.ucfirst(word_list.filter(Q(var_name = 'dont-you-have-an-account'))[0].translation)
    page_dict["alreadyhaveaccount"] = fun.ucfirst(word_list.filter(Q(var_name = 'already-have-account'))[0].translation)
    page_dict["name"] = fun.ucfirst(word_list.filter(Q(var_name = 'name'))[0].translation)
    page_dict["surname"] = fun.ucfirst(word_list.filter(Q(var_name = 'surname'))[0].translation)
    page_dict["username"] = fun.ucfirst(word_list.filter(Q(var_name = 'username'))[0].translation)
    page_dict["password"] = fun.ucfirst(word_list.filter(Q(var_name = 'password'))[0].translation)
    page_dict["emailorphone"] = fun.ucfirst(word_list.filter(Q(var_name = 'email-or-phone'))[0].translation)
    page_dict["signinwithgoogle"] = word_list.filter(Q(var_name = 'signin-with-google'))[0].translation
    page_dict["signinwithfacebook"] = word_list.filter(Q(var_name = 'signin-with-facebook'))[0].translation
    page_dict["signinwithtwitter"] = word_list.filter(Q(var_name = 'signin-with-twitter'))[0].translation
    page_dict["signupwithgoogle"] = word_list.filter(Q(var_name = 'signup-with-google'))[0].translation
    page_dict["signupwithfacebook"] = word_list.filter(Q(var_name = 'signup-with-facebook'))[0].translation
    page_dict["signupwithtwitter"] = word_list.filter(Q(var_name = 'signup-with-twitter'))[0].translation
    page_dict["optional"] = fun.ucfirst(word_list.filter(Q(var_name = 'optional'))[0].translation)
    page_dict["usernamelengtherror"] = word_list.filter(Q(var_name = 'username-length-error'))[0].translation
    page_dict["usernamespecialcharerror"] = word_list.filter(Q(var_name = 'username-specialchar-error'))[0].translation
    page_dict["usernameexistserror"] = word_list.filter(Q(var_name = 'username-exists-error'))[0].translation
    page_dict["usernameonlynumberserror"] = word_list.filter(Q(var_name = 'username-onlynumbers-error'))[0].translation
    page_dict["checkcodemsg"] = word_list.filter(Q(var_name = 'check-code-msg'))[0].translation
    page_dict["enterauthcode"] = word_list.filter(Q(var_name = 'enter-auth-code'))[0].translation
    page_dict["verify"] = fun.ucfirst(word_list.filter(Q(var_name = 'verify'))[0].translation)
    page_dict["resendcode"] = word_list.filter(Q(var_name = 'resend-code'))[0].translation
    page_dict["acceptedtermscondsonsignup"] = word_list.filter(Q(var_name = 'accepted-terms-conds-onsignup'))[0].translation
    page_dict["emailplaceholder"] = word_list.filter(Q(var_name = 'email-placeholder'))[0].translation
    page_dict["resetpassword"] = word_list.filter(Q(var_name = 'reset-password'))[0].translation
    page_dict["havingtroubleloggingin"] = word_list.filter(Q(var_name = 'having-trouble-logging-in'))[0].translation
    page_dict["resetpassinfo"] = word_list.filter(Q(var_name = 'reset-pass-info'))[0].translation
    page_dict["passresetemailsentmsg"] = word_list.filter(Q(var_name = 'pass-reset-email-sent-msg'))[0].translation
    return page_dict


'''---------------------------------------
  HELPERS              
-----------------------------------------'''
def setup_pollmeta(post, word_list):
    current_uid = 8
    post.poll_duration = PostMeta.objects.filter(Q(post_id=post.ID)).filter(Q(meta_key="poll_duration"))[0].meta_value
    post.number_options = int(PostMeta.objects.filter(Q(post_id=post.ID)).filter(Q(meta_key="number_options"))[0].meta_value)
    options_keys = []
    for i in range(0, post.number_options):
        options_keys.append(f'secenek_{i+1}')
    post.poll_options = PostMeta.objects.filter(Q(post_id=post.ID)).filter(Q(meta_key__in=options_keys))
    post.votes = SossyComments.objects.filter(Q(post_id=post.ID))
    total_votes = len(post.votes)
    index = 1
    max_vote = 0
    for vote in post.poll_options:
        vote.num_votes = len(SossyComments.objects.filter(Q(post_id=post.ID)).filter(Q(choice=index)))
        if vote.num_votes > max_vote:
            max_vote = vote.num_votes
        if total_votes == 0:
            vote.percentage = 0
        else:
            vote.percentage = vote.num_votes / total_votes * 100
        index += 1
    for vote in post.poll_options:
        if vote.num_votes == max_vote:
            vote.max_voted = True
            break
    isvoted = SossyComments.objects.filter(Q(post_id=post.ID)).filter(Q(user_id=current_uid))
    if(len(isvoted)>0):
        post.voted = isvoted[0].choice
    duration = PostMeta.objects.filter(Q(post_id=post.ID)).filter(Q(meta_key="poll_duration"))[0].meta_value
    if duration == "Unlimited":
        post.poll_duration_left = fun.ucwords(word_list.filter(Q(var_name = 'unlimited-time'))[0].translation)
    else:
        days = int(duration.split()[0])
        ago = fun.localized_lower(word_list.filter(Q(var_name = 'ago'))[0].translation)
        left = fun.localized_lower(word_list.filter(Q(var_name = 'left'))[0].translation)
        to = post.post_date.replace(tzinfo=None) + dt.timedelta(days=days)
        now = dt.datetime.now()
        if now < to:
            post.poll_duration_left = fun.humanizedate(now, word_list, to=to).replace(ago, left)
        else:
            post.poll_duration_left = "bitti"       

def setup_postmeta(post, word_list):
    current_uid = 8
    post.like = len(PostRating.objects.filter(Q(post_id=post.ID)).filter(Q(opinion='like')))
    post.dislike = len(PostRating.objects.filter(Q(post_id=post.ID)).filter(Q(opinion='dislike')))
    post.rating = post.like - post.dislike
    post.repost = len(Repost.objects.filter(Q(post_id=post.ID)))
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{post.author_id}')
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(post.author_id) + "/" + onlyfiles[0]
    post.author.set_avatar(avatar_url)
    post.time_diff = fun.humanizedate(post.post_date.replace(tzinfo=None), word_list)
    soup = BSHTML(post.post_content,features="html.parser")
    images = soup.findAll('img')
    post.post_images = []
    featured_img = PostMeta.objects.filter(Q(post_id=post.ID)).filter(Q(meta_key="_thumbnail_id"))
    if len(featured_img) > 0:
        featured_id = featured_img[0].meta_value
        featured_img = Post.objects.filter(Q(ID=featured_id))[0].guid
        post.post_images.append(featured_img)
    for img in images:
        post.post_images.append(img['src'])
    if len(post.post_images) == 0:
        post.preview = "not-found"
    else:
        post.preview = post.post_images[0]
    short_content = post.post_content
    short_content = re.sub("(<img.*?>)", "", short_content, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    short_content = fun.striphtml(short_content).replace('\n', '').rstrip()
    post.short_content = short_content
    post.comments = Comment.objects.filter(Q(comment_post_ID=post.ID))
    if (post.post_parent == 0):
        post.parent_title = post.post_title
    else:
        post.parent_title = Post.objects.filter(Q(ID=post.post_parent))[0].post_title

    israted = PostRating.objects.filter(Q(post_id=post.ID)).filter(Q(user_id=current_uid))
    if len(israted) > 0:
        post.user_rate = israted[0].opinion
    if post.post_type == "poll":
        setup_pollmeta(post, word_list)

def morefollowedlists(request):
    try:
        offset = int(request.GET["offset"])
        limit = int(request.GET["limit"])
    except:
        offset = 0
        limit = 3
    limit += 1
    current_uid = 8
    list_ids = ListUser.objects.filter(Q(user_id=current_uid)).order_by('-date')
    list_ids = list({x.list_id: x for x in list_ids}.keys())
    followedlists = List.objects.filter(Q(ID__in=list_ids)).order_by('-created_at')
    if (len(followedlists) < offset):
        return render(request, 'morefollowedlists.html')
    else:
        if (len(followedlists) > limit):
            followedlists = followedlists[offset:limit]
        elif (len(followedlists) >= offset):
            followedlists = followedlists[offset:]
        return render(request, 'lists/morefollowedlists.html', {'limit':limit, 'followedlists':followedlists})

def setup_current_user(current_uid):
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.set_avatar(avatar_url)
    return current_user

'''---------------------------------------
  OPERATIONS              
-----------------------------------------'''
def votepoll(request):
    post_id = request.POST["post_id"]
    user_id = 8
    lang = UserMeta.objects.filter(Q(user_id = user_id)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    choice = request.POST["option"]
    comment = ""
    new_vote = SossyComments(post_id=post_id, user_id=user_id, choice=choice, comment=comment)
    new_vote.save()
    html_string = " <div class='bsbb full-width'>"
    poll = Post.objects.filter(Q(ID=post_id))[0]
    setup_postmeta(poll,word_list)
    post_template_dict = post_template(word_list)
    index = 1
    for poll_option in poll.poll_options:
        html_string += "<div class='bsbb full-width p10 m10'>"
        if poll.voted == index:
            html_string += "<p style='z-index:9;margin-left:40px;padding-right:30px;'>"
            html_string += poll_option.meta_value
            html_string += "<span style='margin-left:20px;width:20px;height:20px;top:1.5px;'><i class='fas fa-check' style='font-size:10px;color:var(--main-color); border:1px solid var(--main-color);border-radius:50%;padding:3px;'></i></span></p>"
        else:
            html_string += "<p style='z-index:9;margin-left:40px;'>"
            html_string += poll_option.meta_value
            html_string += '</p>'
        if poll_option.max_voted:
            html_string += "<p class='absolute' style='top:0;left:0;height:100%;background-color:rgba(0,164,236,0.25);width:"
            html_string += str(poll_option.percentage)
            html_string += "%;border-radius:4px;'>"
            html_string += "<span style='margin-left:20px;line-height:38px;font-size:14px;font-weight:bold;color:var(--dark-gray);top:2px;'>"
            html_string += str(poll_option.num_votes)
            html_string += "</span></p>"
        else:
            html_string += "<p class='absolute' style='top:0;left:0;height:100%;background-color:rgba(0,164,236,0.10);width:"
            html_string += str(poll_option.percentage)
            html_string += "%;border-radius:4px;'><span style='margin-left:20px;line-height:38px;font-size:14px;font-weight:bold;color:var(--dark-gray);'>"
            html_string += str(poll_option.num_votes)
            html_string += "</span></p>"
        html_string += "</div>"
        index += 1
    html_string += "<div class='full-width bt mt10'></div><div class='bsbb full-width p10 inline-flex'>"
    if len(poll.votes) == 1:
        html_string += "<p class='noselect' style='color:var(--gray2);line-height:40px;font-size:13px;'>"
        html_string += str(len(poll.votes))
        html_string += post_template_dict["votenoun"] + "<span style='font-size:10px;margin: 0 4px;'> &#10625; </span>"
        html_string += poll.poll_duration_left
        html_string += "</p>"
    else:
        html_string += "<p class='noselect' style='color:var(--gray2);line-height:40px;font-size:13px;'>"
        html_string += str(len(poll.votes))
        html_string += post_template_dict["votesnoun"] + "<span style='font-size:10px;margin: 0 4px;'> &#10625; </span>"
        html_string += poll.poll_duration_left
        html_string += "</p>"
    html_string += "</div></div>"
    response_data = {}
    response_data['content'] = html_string                          
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_protect
def postrating(request):
    redirect = request.POST["redirect"]
    operation = request.POST["operation"]
    post_id = request.POST["post_id"]
    user_id = 8
    opinion = request.POST["opinion"]
    date = dt.datetime.now()
    if operation == "add":
        olds = PostRating.objects.filter(Q(post_id=post_id)).filter(Q(user_id=user_id))
        for old in olds:
            old.delete()
        new_vote = PostRating(post_id=post_id, user_id=user_id, opinion=opinion, date=date)
        new_vote.save()
    else:
        olds = PostRating.objects.filter(Q(post_id=post_id)).filter(Q(user_id=user_id))
        for old in olds:
            old.delete()
    return HttpResponseRedirect(redirect)

@csrf_exempt
def uploadmedia(request):
    form = MediaFileUploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        photo = form.save()
        form = MediaFileUploadForm()
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)

@csrf_exempt
def uploadmediagetcolor(request):
    print("uploadmediagetcolor")
    form = MediaFileUploadForm(data=request.POST, files=request.FILES)
    print(form.errors)
    if form.is_valid():
        photo = form.save()
        form = MediaFileUploadForm()
        color_thief = ColorThief("static/assets/"+photo.file.name)
        dominant_color = color_thief.get_color(quality=1)
        (r, g, b) = dominant_color
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url, 'color': 'rgb('+str(r)+','+str(g)+','+str(b)+')'}
    else:
        data = {'is_valid': False}
    print(data)
    return HttpResponse(json.dumps(data),content_type="application/json")

def savenewlist(request):
    print("savenewlist")
    photo_url = request.POST["photo_url"]
    filename, file_extension = os.path.splitext(photo_url)
    title = request.POST["title"]
    desc = request.POST["desc"]
    color = request.POST["color"]
    is_public = request.POST["privacy"]
    fun.resize_image(photo_url, "list")
    url = abs(hash(title))
    while List.objects.filter(url=url).exists():
        url += 1
    photo_small = filename + '_40x40' + file_extension
    photo_medium = filename + '_60x60' + file_extension
    photo_large = filename + '_130x130' + file_extension
    creator = 8
    new_list = List(photo_small=photo_small, photo_medium=photo_medium, photo_large=photo_large, name=title, description=desc, creator=creator, color=color, is_public=is_public, created_at=dt.datetime.now(), url=url)
    new_list.save()
    response_data = {}
    response_data['content'] = "success"                        
    return HttpResponse(json.dumps(response_data),content_type="application/json")

def follow_unfollow_list(request):
    redirect = request.POST["redirect"]
    print(request.POST["redirect"])
    list_id = request.POST["list_id"]
    operation = request.POST["operation"]
    user_id = 8
    if operation == "follow":
        new_follower = ListUser(list_id=list_id, user_id=user_id, role="follower", notifications=1, date=dt.datetime.now())
        new_follower.save()
    elif operation == "unfollow":
        instance = ListUser.objects.get(list_id=list_id, user_id=user_id)
        instance.delete()
    return HttpResponseRedirect(redirect)

def savethepost(request):
    try:
        redirect = request.POST["redirect"]
        post_id = request.POST["post_id"]
        user_id = request.POST["user_id"]
        operation = request.POST["operation"]
        if operation == "save":
            instance = SavedPosts(post_id=post_id, user_id=user_id, saved_at=dt.datetime.now())
            instance.save()
        elif operation == "remove":
            instance = SavedPosts.objects.get(post_id=post_id, user_id=user_id)
            instance.delete()
        return HttpResponseRedirect(redirect)
    except:
        return HttpResponseRedirect("")

def savenewcommunity(request):
    print("savenewcommunity")
    title = request.POST["title"]
    # Check if community name is in use:
    creator = 8
    result = Community.objects.filter(name__iexact=title)
    response_data = {}
    lang = UserMeta.objects.filter(Q(user_id = creator)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if(len(result) > 0):
        response_data['content'] = fun.ucfirst(word_list.filter(Q(var_name = 'community-name-inuse-error'))[0].translation) 
    else:
        profile_img = request.POST["profileImgUrl"]
        cover_img = request.POST["coverImgUrl"]
        filename, file_extension = os.path.splitext(profile_img)
        desc = request.POST["desc"]
        color = request.POST["imgColor"]
        is_public = request.POST["isPrivate"]
        nsfw = request.POST["nsfw"]
        primary_cat = request.POST["pricat"]
        related_topics = request.POST["relatedTopics"].split(", ")
        if(is_public == 0):
            is_public = "private"
        elif(is_public == 1):
            is_public = "restricted"
        else:
            is_public = "public"
        fun.resize_image(profile_img, "community")
        photo_small = filename + '_40x40' + file_extension
        photo_large = filename + '_130x130' + file_extension
        try:
            new_community = Community(name=title, slug=title, description=desc, cover_color=color, is_public=is_public, nsfw=nsfw, cover_img=cover_img, profile_img=photo_large, profile_img_small=photo_small)
            new_community.save()
            new_community = Community.objects.get(name=title)
            print(new_community.term_id)
            new_moderator = FollowedCommunities(term_id=new_community.term_id, user_id=creator, role="Moderator", date=dt.datetime.now())
            new_moderator.save()
            new_category = CommunityCategoryRelation(community_id=new_community.term_id, category_id=primary_cat, relation=0)
            new_category.save()
            for i in related_topics:
                new_category = CommunityCategoryRelation(community_id=new_community.term_id, category_id=int(i), relation=1)
                new_category.save()
            response_data['content'] = "success"
        except:
            response_data['content'] = word_list.filter(Q(var_name = 'general-error-msg'))[0].translation                
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def checkusername(request):
    try:
        username = request.POST.get("username")
        user = User.objects.filter(Q(user_login=username))
        if(len(user) > 0):
            data = {'is_valid': False}
        else:
            data = {'is_valid': True}
    except:
        data = {'is_valid': False}
    return JsonResponse(data)

'''---------------------------------------
  VIEWS              
-----------------------------------------'''
def opensosyorol(request):
    try:
        uid = request.session["uid"]
        user = auth.get_user(uid)
        print('Successfully fetched user data: {0}'.format(user.uid))
        return home(request)
    except:
        pass
    try:
        uid = request.POST.get("uid")
        request.session["uid"] = uid
        user = auth.get_user(uid)
        print('Successfully fetched user data: {0}'.format(user.uid))
        return home(request)
    except:
        pass
    lang = "en-EN"
    dark = ""
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    page_dict = sign_dictionary(word_list)
    return render(request, 'signin.html', {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict})

def signin(request):
    return opensosyorol(request)

def signup(request):
    try:
        uid = request.session["uid"]
        user = auth.get_user(uid)
        return HttpResponseRedirect("/")
    except:
        pass
    lang = "en-EN"
    dark = ""
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    page_dict = sign_dictionary(word_list)
    return render(request, 'signup.html', {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict})

def signout(request):
    try:
        redirect = request.POST.get("uid")
        request.session["uid"] = None
        return HttpResponseRedirect(redirect)
    except:
        return HttpResponseRedirect("/")

def resetpassword(request):
    try:
        uid = request.session["uid"]
        user = auth.get_user(uid)
        return HttpResponseRedirect("/")
    except:
        pass   
    lang = "en-EN"
    dark = ""
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    page_dict = sign_dictionary(word_list)
    return render(request, "resetpassword.html", {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict }) 

def verifyresetpassword(request):
    try:
        uid = request.session["uid"]
        user = auth.get_user(uid)
        return HttpResponseRedirect("/")
    except:
        pass   
    lang = "en-EN"
    dark = ""
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    page_dict = sign_dictionary(word_list)
    return render(request, "verifyresetpassword.html", {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict }) 

def phonecodeverification(request):
    try:
        uid = request.session["uid"]
        user = auth.get_user(uid)
        return HttpResponseRedirect("/")
    except:
        pass
    lang = "en-EN"
    dark = ""
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    page_dict = sign_dictionary(word_list)
    phone = request.POST.get("signup_email")
    username = request.POST.get("username")
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    country_code = request.POST.get("country_code")
    phone_code = str(Country.objects.filter(Q(iso=country_code))[0].phonecode)
    if phone_code[0] != "+":
        for i in range(0, len(phone_code)):
            if phone.find(phone_code[i:]) == 0:
                phone = "+" + phone_code[0:i] + phone
                break
    return render(request, "phoneverification.html", {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict, 'phone':phone, 'username':username, 'firstname':firstname, 'lastname': lastname })

def home(request):
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    right_menu_dict = right_menu(word_list)
    feed_dict = feed(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    
    myprofile = fun.ucfirst(word_list.filter(Q(var_name = 'my-profile'))[0].translation)
    createpost = fun.ucfirst(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    seeall = fun.ucfirst(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    populercommunities = fun.ucfirst(word_list.filter(Q(var_name = 'popular-communities'))[0].translation)
    subscribe = fun.ucfirst(word_list.filter(Q(var_name = 'subscribe'))[0].translation)

    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    
    popular_communities = TermTaxonomy.objects.filter(Q(taxonomy="post_tag")).order_by('-count')[:5].prefetch_related()

    post_template_dict = post_template(word_list)
    posts = Post.objects.filter(Q(post_type="post")).filter(Q(post_status="publish")).order_by('-post_date')[1055:1056].prefetch_related()
    for post in posts:
        setup_postmeta(post, word_list)

    links = Post.objects.filter(Q(post_type="link")).filter(Q(post_status="publish")).order_by('-post_date')[:1].prefetch_related()
    for post in links:
        setup_postmeta(post, word_list)
        post.photo_from_url = fun.get_photo_from_url(post.post_content)

    answers = Post.objects.filter(Q(post_type="answer")).filter(Q(post_status="publish")).order_by('-post_date')[:2].prefetch_related()
    for post in answers:
        setup_postmeta(post, word_list)

    questions = Post.objects.filter(Q(post_type="questions")).filter(Q(post_status="publish")).order_by('-post_date')[:8].prefetch_related()
    for post in questions:
        setup_postmeta(post, word_list)
    
    polls = Post.objects.filter(Q(post_type="poll")).filter(Q(post_status="publish")).order_by('-post_date').prefetch_related()
    for poll in polls:
        setup_postmeta(poll, word_list)

    communities = Community.objects.all()[:10]

    user_queryset = User.objects.all()[:10]
    users = []
    for user in user_queryset:
        user = setup_current_user(user.ID)
        users.append(user)

    comment_editor = comment_editor_dict(word_list)
    return render(request, 'index.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities,
                                            'right_menu_dict':right_menu_dict, 'feed_dict':feed_dict,
                                            'popular_communities':popular_communities, 'posts':posts,
                                            'post_template_dict':post_template_dict, 'comment_editor':comment_editor,
                                            'links':links, 'answers':answers, 'questions':questions,
                                            'communities':communities, 'users':users, 'polls':polls
                                            })

@csrf_exempt
def lists(request):
    limit = 3
    current_uid = 8
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    current_user = setup_current_user(current_uid)
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = fun.ucfirst(c.translation)
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    for i in followed_communities:
        color = CommunityMeta.objects.filter(term_id=i.term_id).filter(meta_key = 'color_up')
        if len(color) == 0 or color[0].meta_value == '':
            i.tag_color = "var(--main-color)"
        else:
            i.tag_color = color[0].meta_value
        
        img_url = CommunityMeta.objects.filter(term_id=i.term_id).filter(meta_key = 'tag_img')
        if len(img_url) == 0 or img_url[0].meta_value == '':
            i.tag_img = ""
        else:
            url_id = img_url[0].meta_value
            i.tag_img = Post.objects.filter(Q(ID=url_id))[0].guid
    lists_dict = lists_achive(word_list)
    list_ids = ListUser.objects.filter(Q(user_id=current_uid)).order_by('-date')
    list_ids = list({x.list_id: x for x in list_ids}.keys())
    followedlists = List.objects.filter(Q(ID__in=list_ids)).order_by('-created_at')
    listsyoumaylike = List.objects.order_by('-created_at')[:3]
    for lst in listsyoumaylike:
        lst.posts = ListPost.objects.filter(Q(list_id=lst.ID))
        lst.members = ListUser.objects.filter(Q(list_id=lst.ID) & Q(role='member'))
        lst.followers = ListUser.objects.filter(Q(list_id=lst.ID) & Q(role='follower'))
    return render(request, 'lists/lists.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities, 'lists_dict':lists_dict,
                                            'listsyoumaylike':listsyoumaylike, 'followedlists':followedlists, 'limit':limit
                                            })

def newpost(request):
    try:
        post_type = request.GET['post']
    except:
        post_type = "post"
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    post_types_dict = post_types(word_list)
    create_post_rules_dict = create_post_rules(word_list)
    tips = fun.ucwords(word_list.filter(Q(var_name = 'tips'))[0].translation)
    create_post_dict = {}
    if(post_type == "poll"):
        create_post_dict = create_poll(word_list)
    newpost_actions_dict = newpost_actions(word_list)
    drafts = Post.objects.filter(Q(author_id=current_uid)).filter(post_status="draft").filter(post_type__in=["post", "questions","poll"]).order_by('post_date')
    for post in drafts:
        setup_postmeta(post, word_list)
    return render(request, 'newpost.html', {'post_type':post_type,'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict, 'post_types_dict':post_types_dict,
                                            'create_post_rules_dict': create_post_rules_dict, 'tips':tips, 'create_post_dict':create_post_dict,
                                            'newpost_actions_dict':newpost_actions_dict, 'drafts':drafts})

def createlist(request):
    current_uid = 8
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.set_avatar(avatar_url)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    tips = fun.ucwords(word_list.filter(Q(var_name = 'tips'))[0].translation)
    create_list_dict = {}
    create_list_dict["public"] = fun.ucwords(word_list.filter(Q(var_name = 'public'))[0].translation)
    create_list_dict["private"] = fun.ucwords(word_list.filter(Q(var_name = 'private'))[0].translation)
    create_list_dict["public_info"] = fun.ucfirst(word_list.filter(Q(var_name = 'public_info'))[0].translation)
    create_list_dict["private_info"] = fun.ucfirst(word_list.filter(Q(var_name = 'private_info'))[0].translation)
    create_list_dict["title"] = fun.ucwords(word_list.filter(Q(var_name = 'title'))[0].translation)
    create_list_dict["title_placeholder"] = fun.ucwords(word_list.filter(Q(var_name = 'list_title_placeholder'))[0].translation)
    create_list_dict["desc_placeholder"] = fun.ucfirst(word_list.filter(Q(var_name = 'list_desc_placeholder'))[0].translation)
    create_list_dict["description"] = fun.ucwords(word_list.filter(Q(var_name = 'description'))[0].translation)
    create_list_dict['cancel'] = fun.ucwords(word_list.filter(Q(var_name = 'cancel'))[0].translation)
    create_list_dict['save'] = fun.ucwords(word_list.filter(Q(var_name = 'save'))[0].translation)
    create_list_dict['clear'] = fun.ucwords(word_list.filter(Q(var_name = 'clear'))[0].translation)
    return render(request, 'lists/newlist.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict, 
                                            'tips':tips, 'create_list_dict':create_list_dict})

def listdetail(request, slug, **kwargs):
    if slug == "undefined":
        return createlist(request)
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    print(fltr)
    if fltr == "post":
        lst.posts = lst.posts.filter(Q(post_type="post"))
    elif fltr == "link":
        lst.posts = lst.posts.filter(Q(post_type="link"))
    elif fltr == "poll":
        lst.posts = lst.posts.filter(Q(post_type="poll"))
    elif fltr == "quiz":
        lst.posts = lst.posts.filter(Q(post_type="quiz"))
    elif fltr == "answer":
        lst.posts = lst.posts.filter(Q(post_type="answer"))
    elif fltr == "question":
        lst.posts = lst.posts.filter(Q(post_type="question"))
    elif fltr == "media":
        lst.posts = lst.posts.filter(Q(post_type="media"))
    elif fltr == "about":
        return aboutlist(request, slug)
    elif fltr == "create":
        return createlist(request)
    
    lst = List.objects.get(url=slug)
    post_ids = ListPost.objects.filter(Q(list_id=lst.ID))
    lst.members = ListUser.objects.filter(Q(list_id=lst.ID, role="member"))
    lst.followers = ListUser.objects.filter(Q(list_id=lst.ID, role="follower"))
    current_uid = 8
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.set_avatar(avatar_url)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    lst.posts = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')
    if lst.creator == current_uid:
        lst.is_mine = True

    for post in lst.posts:
        setup_postmeta(post, word_list)
        if post.post_type == "link":
            post.photo_from_url = fun.get_photo_from_url(post.post_content)

    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    right_menu_dict = right_menu(word_list)
    list_dict = lists_achive(word_list)
    post_types_dict = post_types(word_list)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    return HttpResponse(render(request, 'lists/list_detail.html', {'list':lst, 'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'list_dict':list_dict, 'post_types_dict':post_types_dict,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'filter':fltr}))

def listdetailfilter(request, slug, post_type):
    print("listdetailfilter")
    lst = List.objects.get(url=slug)
    post_ids = ListPost.objects.filter(Q(list_id=lst.ID))
    lst.members = ListUser.objects.filter(Q(list_id=lst.ID, role="member"))
    lst.followers = ListUser.objects.filter(Q(list_id=lst.ID, role="follower"))
    current_uid = 8
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.set_avatar(avatar_url)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    lst.posts = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')
    fltr = post_type
    if fltr == "post":
        lst.posts = lst.posts.filter(Q(post_type="post"))
    elif fltr == "link":
        lst.posts = lst.posts.filter(Q(post_type="link"))
    elif fltr == "poll":
        lst.posts = lst.posts.filter(Q(post_type="poll"))
    elif fltr == "quiz":
        lst.posts = lst.posts.filter(Q(post_type="quiz"))
    elif fltr == "answer":
        lst.posts = lst.posts.filter(Q(post_type="answer"))
    elif fltr == "question":
        lst.posts = lst.posts.filter(Q(post_type="question"))
    elif fltr == "media":
        lst.posts = lst.posts.filter(Q(post_type="media"))
    elif fltr == "about":
        return aboutlist(request, slug)
    elif fltr == "create":
        return createlist(request)

    for post in lst.posts:
        setup_postmeta(post, word_list)
        if post.post_type == "link":
            post.photo_from_url = fun.get_photo_from_url(post.post_content)

    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    right_menu_dict = right_menu(word_list)
    list_dict = lists_achive(word_list)
    post_types_dict = post_types(word_list)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    return HttpResponse(render(request, 'lists/list_detail.html', {'list':lst, 'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'list_dict':list_dict, 'post_types_dict':post_types_dict,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'filter':fltr}))

def aboutlist(request, slug):
    lst = List.objects.get(url=slug)
    post_ids = ListPost.objects.filter(Q(list_id=lst.ID))
    lst.members = ListUser.objects.filter(Q(list_id=lst.ID, role="member"))
    lst.followers = ListUser.objects.filter(Q(list_id=lst.ID, role="follower"))
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    lst.posts = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')
    lst.creator_uname = User.objects.filter(Q(ID = lst.creator))[0].user_login
    current_uid = 8
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.set_avatar(avatar_url)
    followed = ListUser.objects.filter(Q(user_id=current_uid)).filter(Q(list_id=lst.ID))
    if len(followed) > 0:
        lst.is_followed = True
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    right_menu_dict = right_menu(word_list)
    list_dict = lists_achive(word_list)
    post_types_dict = post_types(word_list)
    list_info_dict = list_info(word_list)
    return render(request, 'lists/aboutlist.html', {'list':lst, 'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'list_dict':list_dict, 'post_types_dict':post_types_dict,
                                            'list_info_dict':list_info_dict})

def savedposts(request, **kwargs):
    current_uid = 8
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = fun.ucfirst(c.translation)
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.set_avatar(avatar_url)

    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    for i in followed_communities:
        color = CommunityMeta.objects.filter(term_id=i.term_id).filter(meta_key = 'color_up')
        if len(color) == 0 or color[0].meta_value == '':
            i.tag_color = "var(--main-color)"
        else:
            i.tag_color = color[0].meta_value
        
        img_url = CommunityMeta.objects.filter(term_id=i.term_id).filter(meta_key = 'tag_img')
        if len(img_url) == 0 or img_url[0].meta_value == '':
            i.tag_img = ""
        else:
            url_id = img_url[0].meta_value
            i.tag_img = Post.objects.filter(Q(ID=url_id))[0].guid
    savedpostsobjs = SavedPosts.objects.filter(Q(user_id=current_uid)).prefetch_related()
    savedposts = []
    for item in savedpostsobjs:
        if fltr == "all" or item.post.post_type == fltr:
            setup_postmeta(item.post, word_list)
            if item.post.post_type == "link":
                item.post.photo_from_url = fun.get_photo_from_url(item.post.post_content)
            savedposts.append(item.post)
    savedposts_dict = {}
    savedposts_dict["saveditems"] = fun.ucfirst(word_list.filter(Q(var_name = 'saveditems'))[0].translation)
    savedposts_dict["saveditemsDesc"] = fun.ucfirst(word_list.filter(Q(var_name = 'saveditemsDesc'))[0].translation)
    savedposts_dict["all"] = fun.ucfirst(word_list.filter(Q(var_name = 'all'))[0].translation)
    post_types_dict = post_types(word_list)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    right_menu_dict = right_menu(word_list)
    users = User.objects.all()[:2]
    for user in users:
        user_desc = UserMeta.objects.filter(Q(user_id = user.ID)).filter(Q(meta_key = 'description'))[0]
        user.set_description(user_desc.meta_value)
        mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{user.ID}')
        if (os.path.exists(mypath)):
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(user.ID) + "/" + onlyfiles[0]
        else:
            avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        user.set_avatar(avatar_url)
    return render(request, "savedposts.html", {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities, 'savedposts_dict':savedposts_dict,
                                            'post_types_dict':post_types_dict, 'savedposts':savedposts, 'filter': fltr,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'right_menu_dict':right_menu_dict, 'users':users
                                            })

def savedpostsfilter(request, post_type):
    return savedposts(request, filter=post_type)

def communitydetail(request, slug,  **kwargs):
    if slug == "lists":
        return lists(request)
    elif slug == "communities/create":
        return newcommunity(request)

    community = Community.objects.filter(slug=slug)[0]
    taxonomy = TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
    post_ids = TermRelationship.objects.filter(Q(term_taxonomy_id=taxonomy))
    post_ids = list({x.object_id: x for x in post_ids}.keys())
    community.posts = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    if fltr == "post":
        community.posts = community.posts.filter(Q(post_type="post"))
    elif fltr == "link":
        community.posts = community.posts.filter(Q(post_type="link"))
    elif fltr == "poll":
        community.posts = community.posts.filter(Q(post_type="poll"))
    elif fltr == "quiz":
        community.posts = community.posts.filter(Q(post_type="quiz"))
    elif fltr == "answer":
        community.posts = community.posts.filter(Q(post_type="answer"))
    elif fltr == "question":
        community.posts = community.posts.filter(Q(post_type="question"))
    elif fltr == "media":
        community.posts = community.posts.filter(Q(post_type="media"))


    community.posts = community.posts[:20]

    community.flairs = Flairs.objects.filter(term_id=community.term_id).filter(flair_type="post")

    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    for post in community.posts:
        setup_postmeta(post, word_list)
        if post.post_type == "link":
            post.photo_from_url = fun.get_photo_from_url(post.post_content)
    header_dict = header(word_list)
    post_types_dict = post_types(word_list)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    feed_dict = feed(word_list)
    followers = FollowedCommunities.objects.filter(Q(term_id=community.term_id))
    followings = []
    for f in followers:
        user = UserRelation.objects.filter(Q(following_id=f.user_id)).filter(Q(follower_id=current_uid))
        if (len(user) > 0):
            user[0].following = setup_current_user(user[0].following.ID)
            followings.append(user[0])
    page_dict = communitydetail_dict(word_list, 83, followings)
    moderators = followers.filter(role="moderator")
    for m in moderators:
        m.user = setup_current_user(m.user_id)
    return render(request, 'communities/communitydetail.html', {'header_dict':header_dict, 'community':community,
                                                                'post_types_dict':post_types_dict, 'filter':fltr,
                                                                'feed_dict':feed_dict, 'page_dict':page_dict,
                                                                'followers':followers, 'comment_editor':comment_editor,
                                                                'post_template_dict': post_template_dict, 'followings':followings,
                                                                'moderators':moderators, 'current_user': current_user
                                                                })

def newcommunity(request):
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    tips = fun.ucwords(word_list.filter(Q(var_name = 'tips'))[0].translation)
    communitycats = CommunityCategories.objects.all().order_by("name")
    create_list_dict = create_community(word_list)
    new_community_tips_dict = new_community_tips(word_list)
    return render(request, 'communities/newcommunity.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict, 
                                            'tips':tips, 'create_list_dict':create_list_dict, 'communitycats':communitycats,
                                            'new_community_tips_dict':new_community_tips_dict})


