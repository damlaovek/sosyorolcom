from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from sosyorol.models import *
from django.db.models import Q
import os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup as BSHTML
import datetime as dt
from urllib.request import urlopen
import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import time
import requests
import sosyorol.functions as fun
#import firebase_admin
#from firebase_admin import auth, credentials
from itertools import chain
from django.views.generic.list import ListView
from django.db.models import Count
from django.core.cache import cache
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')

current_uid = None

'''---------------------------------------
  FIREBASE              
-----------------------------------------'''
"""
if not firebase_admin._apps:
    cred = credentials.Certificate('static/sosyorol-b6ab6-firebase-adminsdk-q80t3-54150f4057.json') 
    default_app = firebase_admin.initialize_app(cred)
    auth = default_app.auth()
"""

'''---------------------------------------
  DICTIONARIES              
-----------------------------------------'''
def left_menu(word_list):
    left_menu_dict = {}
    left_menu_dict['createpost'] = word_list.get(var_name = 'create-post').translation
    left_menu_dict['feed'] = word_list.get(var_name = 'feed').translation
    left_menu_dict['darkmode'] = word_list.get(var_name = 'dark-mode').translation
    left_menu_dict['lightmode'] = word_list.get(var_name = 'light-mode').translation
    left_menu_dict['country'] = word_list.get(var_name = 'lang').translation
    left_menu_dict['about'] = word_list.get(var_name = 'about').translation
    left_menu_dict['careers'] = word_list.get(var_name = 'careers').translation
    left_menu_dict['advertise'] = word_list.get(var_name = 'advertise').translation
    left_menu_dict['helpvar'] = word_list.get(var_name = 'help').translation
    left_menu_dict['termsvar'] = word_list.get(var_name = 'terms').translation
    left_menu_dict['createlist'] = word_list.get(var_name = 'create-list').translation
    left_menu_dict['lists'] = word_list.get(var_name = 'lists').translation
    left_menu_dict['visithistory'] = word_list.get(var_name = 'visithistory').translation
    left_menu_dict['savedposts'] = word_list.get(var_name = 'savedposts').translation
    left_menu_dict['more'] = word_list.get(var_name = 'more').translation
    left_menu_dict['less'] = word_list.get(var_name = 'less').translation
    left_menu_dict['createcommunity'] = word_list.get(var_name = 'create-community').translation
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
    right_menu_dict['interaction'] = word_list.get(var_name = 'interaction').translation
    right_menu_dict['scrolltotop'] = word_list.get(var_name = 'scroll-to-top').translation
    right_menu_dict['viewprofile'] = word_list.get(var_name = 'go-to-profile').translation
    right_menu_dict['myprofile'] = word_list.get(var_name = 'my-profile').translation
    right_menu_dict['createpost'] = word_list.get(var_name = 'create-post').translation
    right_menu_dict['seeall'] = word_list.get(var_name = 'see-all').translation
    right_menu_dict['popularcommunities'] = word_list.get(var_name = 'popular-communities').translation
    right_menu_dict['subscribe'] = word_list.get(var_name = 'subscribe').translation
    right_menu_dict['trendsofcountrytitle'] = word_list.get(var_name = 'trends-of-country-title').translation
    right_menu_dict['showmore'] = word_list.get(var_name = 'show-more').translation
    right_menu_dict['usersyoumayfollow'] = word_list.get(var_name = 'users-you-may-follow').translation
    right_menu_dict['follow'] = word_list.get(var_name = 'follow').translation
    right_menu_dict['createcommunity'] = word_list.get(var_name = 'create-community').translation
    return right_menu_dict

def feed(word_list):
    feed_dict = {}
    feed_dict['hiddentakeback'] = word_list.get(var_name = 'hidden-take-back').translation
    feed_dict['hiddenusers'] = word_list.get(var_name = 'hidden-users').translation
    feed_dict['media'] = word_list.get(var_name = 'media').translation
    feed_dict['link'] = word_list.get(var_name = 'link').translation
    feed_dict['quiz'] = word_list.get(var_name = 'quiz').translation
    feed_dict['poll'] = word_list.get(var_name = 'poll').translation
    feed_dict['question'] = word_list.get(var_name = 'question').translation
    feed_dict['follow'] = word_list.get(var_name = 'follow').translation
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
    post_template_dict['article'] = fun.ucwords(word_list.get(var_name = 'article').translation)
    post_template_dict['media'] = fun.ucwords(word_list.get(var_name = 'media').translation)
    post_template_dict['link'] = fun.ucwords(word_list.get(var_name = 'link').translation)
    post_template_dict['answer'] = fun.ucwords(word_list.get(var_name = 'answer').translation)
    post_template_dict['question'] = fun.ucwords(word_list.get(var_name = 'question').translation)
    post_template_dict['quiz'] = fun.ucwords(word_list.get(var_name = 'quiz').translation)
    post_template_dict['poll'] = fun.ucwords(word_list.get(var_name = 'poll').translation)
    post_template_dict['answernoun'] = fun.ucwords(word_list.get(var_name = 'answer-noun').translation)
    post_template_dict['recommendedfy'] = fun.ucwords(word_list.get(var_name = 'recommended-for-you').translation)
    post_template_dict['more'] = fun.ucwords(word_list.get(var_name = 'more').translation)
    post_template_dict['share'] = fun.ucwords(word_list.get(var_name = 'share').translation)
    post_template_dict['comments'] = fun.ucwords(word_list.get(var_name = 'comments').translation)
    post_template_dict['repost'] = fun.ucwords(word_list.get(var_name = 'repost').translation)
    post_template_dict['upvote'] = fun.ucwords(word_list.get(var_name = 'upvote').translation)
    post_template_dict['downvote'] = fun.ucwords(word_list.get(var_name = 'downvote').translation)
    post_template_dict['send'] = fun.ucwords(word_list.get(var_name = 'send').translation)
    post_template_dict['subscribe'] = fun.ucwords(word_list.get(var_name = 'subscribe').translation)
    post_template_dict['vote'] = fun.ucwords(word_list.get(var_name = 'vote').translation)
    post_template_dict['votenoun'] = fun.localized_lower(word_list.get(var_name = 'vote-noun').translation)
    post_template_dict['votesnoun'] = fun.localized_lower(word_list.get(var_name = 'votes-noun').translation)
    return post_template_dict

def comment_editor_dict(word_list):
    comment_editor = {}
    comment_editor['addcomment'] = word_list.get(var_name = 'add-comment').translation
    comment_editor['send'] = word_list.get(var_name = 'send').translation
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
    page_dict['views'] = fun.ucfirst(word_list.filter(var_name = 'views')[0].translation)
    page_dict['usersfollowing'] = fun.ucfirst(word_list.filter(var_name = 'users-are-following-this')[0].translation)
    rank = word_list.filter(var_name = 'community-rank-info')[0].translation
    rank = rank.replace("[number]",f"<span class='fwbold'>{community_rank}</span>")
    page_dict['rank'] = rank
    page_dict['join'] = fun.ucfirst(word_list.filter(var_name = 'join')[0].translation)
    page_dict['following'] = fun.ucwords(word_list.filter(var_name = 'following')[0].translation)
    page_dict['moderators'] = fun.ucfirst(word_list.filter(var_name = 'moderators')[0].translation)
    page_dict['showmore'] = fun.ucfirst(word_list.filter(var_name = 'show-more')[0].translation)
    page_dict['filterbylabel'] = fun.ucfirst(word_list.filter(var_name = 'filter-by-label')[0].translation)
    page_dict['communityrules'] = fun.ucfirst(word_list.filter(var_name = 'community-rules')[0].translation)
    if (len(followings) == 0):
        followingsinfo = ""
    elif (len(followings) >= 3):
        followingsinfo = word_list.filter(var_name = 'community-followers-info')[0].translation
        followingsinfo = followingsinfo.replace("[number]", f"{len(followings)}")
    else:
        followingsinfo = word_list.filter(var_name = 'community-followers-info2')[0].translation
        str1 = f"<a href='/u/{followings[0].following.user_nicename}' target='_blank' class='fs13 cg2 lh30 underline-on-hover' style='top:-2.5px;'>u/{followings[0].following.user_nicename}</a>"
        if (len(followings) == 1):
            followingsinfo = followingsinfo.replace("[user] & [user]", str1)
        else:
            str2 = f"<a href='/u/{followings[0].following.user_nicename}' target='_blank' class='fs13 cg2 lh30 underline-on-hover' style='top:-2.5px;'>u/{followings[1].following.user_nicename}</a>"
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
    page_dict["notmatchingpasserror"] = word_list.filter(Q(var_name = 'not-matching-pass-error'))[0].translation
    return page_dict

def search_page_dict(word_list):
    page_dict = {}
    page_dict['all'] = fun.ucfirst(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    page_dict["resultsforthissearch"] = word_list.filter(Q(var_name = 'results-for-this-search'))[0].translation
    page_dict['community'] = fun.ucfirst(word_list.filter(Q(var_name = 'community'))[0].translation)
    page_dict['user'] = fun.ucfirst(word_list.filter(Q(var_name = 'user'))[0].translation)
    page_dict['views'] = fun.ucfirst(word_list.filter(Q(var_name = 'views'))[0].translation)
    page_dict['usersfollowing'] = fun.ucfirst(word_list.filter(Q(var_name = 'users-are-following-this'))[0].translation)
    return page_dict

def history_dict(word_list):
    page_dict = {}
    page_dict["historyPageDesc"] = fun.ucfirst(word_list.filter(Q(var_name = 'historyPageDesc'))[0].translation)
    page_dict['all'] = fun.ucfirst(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    page_dict['searchHistory'] = fun.ucfirst(word_list.filter(Q(var_name = 'search-history'))[0].translation)
    page_dict['community'] = fun.ucfirst(word_list.filter(Q(var_name = 'community'))[0].translation)
    page_dict['user'] = fun.ucfirst(word_list.filter(Q(var_name = 'user'))[0].translation)
    page_dict['historytype'] = word_list.filter(Q(var_name = 'history-type'))[0].translation
    page_dict['clearallhistory'] = word_list.filter(Q(var_name = 'clear-all-history'))[0].translation
    page_dict['views'] = fun.ucfirst(word_list.filter(Q(var_name = 'views'))[0].translation)
    page_dict['usersfollowing'] = fun.ucfirst(word_list.filter(Q(var_name = 'users-are-following-this'))[0].translation)
    return page_dict

'''---------------------------------------
  HELPERS              
-----------------------------------------'''
def get_current_uid(request):
    uid = None
    try:
        uid = request.POST["uid"]
        uid = uid.replace("%40", "@")
        print(uid)
        user = User.objects.get(user_email=uid)
        request.COOKIES["uid"] = str(user.ID)
    except:
        pass
    if 'uid' in request.COOKIES:
        uid = request.COOKIES["uid"]
        if ('%40' in uid) or ('@' in uid):
            uid = uid.replace("%40", "@")
            user = User.objects.get(user_email=uid)
            uid = str(user.ID)
            request.COOKIES["uid"] = uid
        """
        uid = uid.replace("%40", "@")
        print(uid)
        user = User.objects.get(user_email=uid)
        request.COOKIES["uid"] = str(user.ID)
        """
        if uid is None:
            return -1
    else:
        return -1
    if uid is None:
        return -1
    global current_uid
    current_uid = int(request.COOKIES["uid"].replace("sosyoroluseruid", ""))
    return current_uid

def arrange_post_slug(title):
    import string
    import re
    import unidecode
    """
    title = title.lower()
    title = title.replace("ı","i")
    title = title.replace("ç","c")
    title = title.replace("ş","s")
    title = title.replace("ö","o")
    title = title.replace("ü","u")
    title = title.replace("ğ","g")
    title = title.translate(str.maketrans('', '', string.punctuation))
    title = title.replace(' ','_')
    title = title.replace('\'','')
    """
    title = title.replace(" - Sosyorol", "")
    title = unidecode.unidecode(title).lower()
    title = title.translate(str.maketrans('', '', string.punctuation))
    title = title.replace(' ','_')
    title = title.replace('\'','')
    return title

def isquestionanswered(question, user_id):
    answer = Post.objects.filter(post_title=question.post_title, post_status="publish", post_parent=question.ID, post_author=user_id, post_type="answer")
    if answer.count() > 0:
        return True
    return False

def setup_quizmeta(post, word_list):
    import re
    post.quiz_questions = []
    num_questions = int(PostMeta.objects.filter(post_id=post.ID, meta_key="question_number")[0].meta_value)
    for i in range(1, num_questions + 1):
        question = dict()
        question["question_text"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_question")[0].meta_value
        num_answers = int(PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_number")[0].meta_value)
        question["answer_type"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_type")[0].meta_value
        answers = []
        for j in range(1, num_answers + 1):
            answer = dict()
            answer["content"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_content")[0].meta_value
            answer["assoc_result"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_assoc_result")[0].meta_value
            if question["answer_type"] == "colorBox":
                answer["color"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_color")[0].meta_value
            answers.append(answer)
        question["answers"] = answers
        post.quiz_questions.append(question)

def setup_colorbox_quizmeta(post, word_list):
    num_questions = int(PostMeta.objects.filter(post_id=post.ID, meta_key="question_number")[0].meta_value)
    post.quiz_questions = []
    for i in range(1, num_questions + 1):
        question = dict()
        question["question_text"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_question")[0].meta_value
        question["question_color"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_color")[0].meta_value
        num_answers = int(PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_number")[0].meta_value)
        question["answer_type"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_type")[0].meta_value
        answers = []
        for j in range(1, num_answers + 1):
            answer = dict()
            answer["content"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_content")[0].meta_value
            answer["assoc_result"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_assoc_result")[0].meta_value
            if question["answer_type"] == "colorBox":
                answer["color"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_color")[0].meta_value
            answers.append(answer)
        question["answers"] = answers
        post.quiz_questions.append(question)

def setup_media_quizmeta(post, word_list):
    num_questions = int(PostMeta.objects.filter(post_id=post.ID, meta_key="question_number")[0].meta_value)
    post.quiz_questions = []
    for i in range(1, num_questions + 1):
        question = dict()
        question["question_text"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_question")[0].meta_value
        question["question_img"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_img")[0].meta_value
        num_answers = int(PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_number")[0].meta_value)
        question["answer_type"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_type")[0].meta_value
        answers = []
        for j in range(1, num_answers + 1):
            answer = dict()
            answer["content"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_content")[0].meta_value
            answer["assoc_result"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_assoc_result")[0].meta_value
            if question["answer_type"] == "colorBox":
                answer["color"] = PostMeta.objects.filter(post_id=post.ID, meta_key="soru_"+str(i)+"_answer_"+str(j)+"_color")[0].meta_value
            answers.append(answer)
        question["answers"] = answers
        post.quiz_questions.append(question)

def setup_pollmeta(post, word_list):
    post.poll_duration = PostMeta.objects.filter(post_id=post.ID, meta_key="poll_duration")[0].meta_value
    post.number_options = int(PostMeta.objects.filter(post_id=post.ID, meta_key="number_options")[0].meta_value)
    options_keys = []
    for i in range(0, post.number_options):
        options_keys.append(f'secenek_{i+1}')
    post.poll_options = PostMeta.objects.filter(post_id=post.ID, meta_key__in=options_keys)
    post.votes = SossyComments.objects.filter(post_id=post.ID)
    total_votes = post.votes.count()
    index = 1
    max_vote = 0
    for vote in post.poll_options:
        vote.num_votes = SossyComments.objects.filter(post_id=post.ID, choice=index).count()
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
    print(current_uid)
    isvoted = SossyComments.objects.filter(post_id=post.ID, user_id=current_uid)
    print(isvoted)
    if(isvoted.count()>0):
        post.voted = isvoted[0].choice
    duration = PostMeta.objects.filter(post_id=post.ID, meta_key="poll_duration")[0].meta_value
    if duration == "Unlimited" or duration == word_list.get(var_name = 'unlimited-time').translation:
        post.poll_duration_left = word_list.get(var_name = 'unlimited-time').translation
    else:
        days = int(duration.split()[0])
        ago = word_list.get(var_name = 'ago').translation
        left = word_list.get(var_name = 'left').translation
        to = post.post_date.replace(tzinfo=None) + dt.timedelta(days=days)
        now = dt.datetime.now()
        if now < to:
            post.poll_duration_left = fun.humanizedate(now, word_list, to=to).replace(ago, left)
        else:
            post.poll_duration_left = fun.ucfirst(word_list.get(var_name = 'finished').translation)

def setup_mediameta(post):
    post.media_type = PostMeta.objects.filter(post_id=post.ID, meta_key="media_type")[0].meta_value
    post.media_url = PostMeta.objects.filter(post_id=post.ID, meta_key="media_url")[0].meta_value

def setup_postmeta(post, word_list):
    print(post.ID)
    import re
    post.hex_id = hex(post.ID + 100000).replace("x", "s")
    post.post_title = post.post_title.replace(" - Sosyorol", "")
    post.guid = arrange_post_slug(post.post_title)

    post.likes = PostRating.objects.filter(post_id=post.ID, opinion='like')
    post.dislikes = PostRating.objects.filter(post_id=post.ID, opinion='dislike')
    
    start = time.time()
    post.rating = len(post.likes) - len(post.dislikes)
    end = time.time() - start
    
    post.repost = Repost.objects.filter(post_id=post.ID)

    '''community_taxonomy_ids = TermRelationship.objects.filter(Q(object_id=post.ID))
    community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
    community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
    community_ids = list({x.term_id: x for x in community_ids}.keys())
    post.communities = Community.objects.filter(term_id__in=community_ids)
    if post.communities.count() > 0:
        post.first_community = post.communities[0].name'''
    
    start = time.time()
    post.author = User.objects.get(ID=post.post_author)
    end = time.time() - start


    start = time.time()
    post.author.avatar_url = setup_avatar_url(post.post_author)
    end = time.time() - start
    
    #post.time_diff = fun.humanizedate(post.post_date.replace(tzinfo=None), word_list)
    post.time_diff = post.post_date

    if post.post_type == "answer":
        post.parent = Post.objects.filter(ID=post.post_parent)[0]
        post.parent.guid = arrange_post_slug(post.parent.post_title)
        post.parent.hex_id = hex(post.parent.ID + 100000).replace("x", "s")
    if post.post_type == "post" or post.post_type == "answer" or post.post_type == "questions":
        soup = BSHTML(post.post_content,features="html.parser")
        images = soup.findAll('img')
        post.post_images = []
        featured_img = PostMeta.objects.filter(post_id=post.ID, meta_key="_thumbnail_id")
        if featured_img.count() > 0:
            featured_id = featured_img[0].meta_value
            featured_img = Post.objects.get(ID=featured_id).guid
            post.post_images.append(featured_img)
        '''for img in images:
            post.post_images.append(img['src'])'''
        if len(post.post_images) == 0:
            post.preview = "not-found"
        else:
            post.preview = post.post_images[0]
        short_content = post.post_content
        short_content = re.sub("(<img.*?>)", "", short_content, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        short_content = fun.striphtml(short_content).replace('\n', '').rstrip()
        post.short_content = short_content
    post.comments = Comment.objects.filter(comment_post=post)
    if post.post_type == "answer":
        if (post.post_parent == 0):
            post.parent_title = post.post_title
        else:
            post.parent_title = Post.objects.get(ID=post.post_parent).post_title
    israted = PostRating.objects.filter(post_id=post.ID, user_id=current_uid)
    if israted.count() > 0:
        post.user_rate = israted[0].opinion
    
def morefollowedlists(request):
    try:
        offset = int(request.GET["offset"])
        limit = int(request.GET["limit"])
    except:
        offset = 0
        limit = 3
    limit += 1
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

def morecommunities(request):
    try:
        offset = int(request.GET["offset"])
        limit = int(request.GET["limit"])
        fltr = request.GET["filter"]
    except:
        offset = 20
        limit = 20
        fltr = "all"
    hasMore = "True"
    if fltr == "all":
        communities = Community.objects.all()
        if communities.count() < offset :
            return render(request, 'communities/communitytemplates/leaderboard_template.html')
            hasMore = "False"
        elif communities.count() < offset + limit:
            communities = communities[offset:]
            hasMore = "False"
        else:
            communities = communities[offset:(offset + limit)]
    else:
        selected_category = CommunityCategories.objects.get(name=fun.localized_upper(fltr))
        communities = CommunityCategoryRelation.objects.filter(category=selected_category)
        if communities.count() < offset :
            return render(request, 'communities/communitytemplates/leaderboard_template.html')
            hasMore = "False"
        elif communities.count() < offset + limit:
            communities = communities[offset:]
            hasMore = "False"
        else:
            communities = communities[offset:(offset + limit)]
    
    return render(request, 'communities/communitytemplates/leaderboard_template.html', {'communities':communities, 'filter':fltr, 'offset':offset, 'hasMore':hasMore})

@csrf_exempt
def pickpostcommunities(request):
    search_key = request.POST["search"]
    selectedComms = request.POST["selectedComms"]
    selected = selectedComms.split(", ")
    selected = [i for i in selected if i]
    communities = Community.objects.all()
    if len(selected) > 0:
        condition = Q(name=selected[0])
        for string in selected[1:]:
            condition &= Q(name=string)
        communities = communities.exclude(condition)
    communities = communities.filter(name__icontains=search_key)[:10]
    return render(request, 'posts/createpost/communitylist.html', {'communities':communities})

@csrf_exempt
def getcommunityflairs(request):
    community = request.POST["community"]
    comm_obj = Community.objects.filter(name=community)[0]
    flairs = Flairs.objects.filter(term_id=comm_obj.term_id).filter(flair_type="post")
    return render(request, 'posts/createpost/flair.html', {'community':comm_obj, 'flairs': flairs})

def setup_avatar_url(userId):
    avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    try:
        avatar_url = UserMeta.objects.filter(user_id=userId, meta_key="avatar_url")[0].meta_value
    except:
        pass
    return avatar_url

def setup_current_user(cuid):
    current_user = User.objects.filter(ID = cuid)[0]
    try:
        user_desc = UserMeta.objects.filter(user_id = cuid, meta_key = 'description')[0]
        current_user.description = user_desc.meta_value
    except:
        pass
    current_user.posts = Post.objects.filter(post_author=cuid, post_status__in=["publish", "repost"], post_type__in=["post", "quiz", "poll", "answer", "questions", "link", "media", "repost"]).order_by('-post_date')
    current_user.avatar_url = setup_avatar_url(cuid)
    birthday = UserMeta.objects.filter(user=cuid, meta_key="birthday")
    if birthday.count() > 0:
        dateobj = dt.datetime.strptime(birthday[0].meta_value, '%Y-%m-%d')
        current_user.birthday["birthday"] = dateobj.strftime("%d.%m.%Y")
        current_user.birthday["ID"] = birthday[0].umeta_id
    try:
        current_user.followers = UserRelation.objects.filter(following=current_user)
        current_user.followings = UserRelation.objects.filter(follower=current_user)
        current_user.blocked = BlockedUsers.objects.filter(blocker=current_user)
        #{f.follower.avatar_url: setup_avatar_url(f.follower_id) for f in current_user.followers}
        #{f.followings.avatar_url: setup_avatar_url(f.follower_id) for f in current_user.followers}
        #{b.blocking.avatar_url: setup_avatar_url(b.blocking_id) for b in current_user.blocked}
        '''
        for f in current_user.followers:
            try:
                avatar_url = UserMeta.objects.filter(user=f.follower, meta_key="avatar_url")[0].meta_value
                f.follower.avatar_url = avatar_url
            except:
                f.follower.avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        for b in current_user.blocked:
            try:
                avatar_url = UserMeta.objects.filter(user=b.blocking, meta_key="avatar_url")[0].meta_value
                b.blocking.avatar_url = avatar_url
            except:
                b.blocking.avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        '''
    except:
        pass
    return current_user

def setup_notifications(current_uid, word_list, **kwargs):
    notifications = Notification.objects.filter(to_u_id=current_uid).prefetch_related().order_by('-date')
    if 'filter' in kwargs:
        fltr = kwargs.get("filter").split("_")[0]
    else:
        fltr = "all"
    if fltr == "birthday":
        notifications = notifications.filter(notification_variable__in=["birthday", "birthday-old"])
    elif fltr == "follow":
        notifications = notifications.filter(notification_variable="follow")
    elif fltr == "community":
        notifications = notifications.filter(notification_variable="community-post")
    elif fltr == "comment":
        notifications = notifications.filter(notification_variable__in=["comment-reply","comment-on-post"])
    elif fltr == "answer":
        notifications = notifications.filter(notification_variable="answer-question")
    elif fltr == "post":
        notifications = notifications.filter(notification_variable="new-post")
    notifs = dict()
    new_notifs = []
    old_notifs = []
    num_unopened = 0
    for notification in notifications:
        notification.from_u = setup_current_user(notification.from_u_id)
        notification.date_diff = fun.humanizedate(notification.date.replace(tzinfo=None), word_list, to=dt.datetime.now())
        if(notification.opened == 0):
            num_unopened += 1
        notification.notification = word_list.filter(var_name="notification-"+notification.notification_variable)[0].translation
        notification.notification = notification.notification.replace("{user}", "<span class='fwbold'>u/"+notification.from_u.user_login+"</span>")
        if notification.date.day == dt.datetime.today().day and notification.date.month == dt.datetime.today().month and notification.date.year == dt.datetime.today().year:
            new_notifs.append(notification)
        else:
            old_notifs.append(notification)
    notifs["new"] = new_notifs
    notifs["earlier"] = old_notifs
    return notifs, num_unopened

def communitiesfiltered(request, **kwargs):
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    try:
        fromcompage = request.GET["fromcompage"]
        if fromcompage != "yes":
            return communities(request, filter=fltr)
    except:
        return communities(request, filter=fltr)
    if fltr == "all":
        community_list = Community.objects.all()[0:20]
    else:
        selected_category = CommunityCategories.objects.get(slug=fun.localized_upper(fltr))
        community_list = CommunityCategoryRelation.objects.filter(category=selected_category)[:20]
    return render(request, 'communities/communitytemplates/leaderboard.html', {'communities':community_list, 'filter':fltr})

def quizzesfiltered(request, **kwargs):
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    try:
        fromcompage = request.GET["fromcompage"]
        if fromcompage != "yes":
            return quizzes(request, filter=fltr)
    except:
        return quizzes(request, filter=fltr)
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    quiz_list = Post.objects.filter(post_status="publish", post_type="quiz").order_by("-post_date")
    if fltr != "all":
        selected_category = CommunityCategories.objects.get(slug=fun.localized_upper(fltr))
        community_list = CommunityCategoryRelation.objects.filter(category=selected_category)
        community_ids = list({x.community_id: x for x in community_list}.keys())
        taxonomies = TermTaxonomy.objects.filter(term_id__in=community_ids)
        taxonomy_ids = list({x.term_taxonomy_id: x for x in taxonomies}.keys())
        post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomy_ids)
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        quiz_list = quiz_list.filter(ID__in=post_ids)
    for post in quiz_list:
        setup_postmeta(post, word_list)
        post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
        post.post_title = post.post_title.replace(" - Sosyorol", "")
        if post.quiz_type == "media":
            setup_media_quizmeta(post, word_list)
        elif post.quiz_type == "colorBox":
            setup_colorbox_quizmeta(post, word_list)
        else:
            setup_quizmeta(post, word_list)
    return render(request, 'quiz_list.html', {'quizzes':quiz_list, 'filter':fltr, 'word_list':word_list})

def pollsfiltered(request, **kwargs):
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    try:
        fromcompage = request.GET["fromcompage"]
        if fromcompage != "yes":
            return polls(request, filter=fltr)
    except:
        return quizzes(request, filter=fltr)
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    poll_list = Post.objects.filter(post_status="publish", post_type="poll").order_by("-post_date")
    if fltr != "all":
        selected_category = CommunityCategories.objects.get(slug=fun.localized_upper(fltr))
        community_list = CommunityCategoryRelation.objects.filter(category=selected_category)
        community_ids = list({x.community_id: x for x in community_list}.keys())
        taxonomies = TermTaxonomy.objects.filter(term_id__in=community_ids)
        taxonomy_ids = list({x.term_taxonomy_id: x for x in taxonomies}.keys())
        post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomy_ids)
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        poll_list = poll_list.filter(ID__in=post_ids)
    for post in poll_list:
        setup_postmeta(post, word_list)
        community_taxonomy_ids = TermRelationship.objects.filter(Q(object_id=post.ID))
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        post.communities = Community.objects.filter(term_id__in=community_ids)
        if post.communities.count() > 0:
            post.first_community = post.communities[0].name
    return render(request, 'poll_list.html', {'polls':poll_list, 'filter':fltr, 'word_list':word_list})

def addanotherquizresult(request):
    nmr = str(int(request.GET["number"]) + 1)
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    return render(request, 'posts/createpost/quiz_result.html', {'number':nmr, 'word_list':word_list})

def addanotherquizquestion(request):
    nmr = str(int(request.GET["number"]) + 1)
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    qtype = request.GET["type"]
    return render(request, 'posts/createpost/quiz_question.html', {'number':nmr, 'word_list':word_list, 'qtype':qtype})

def getchildcomments(post_id, parent_id):
    comments = Comment.objects.filter(comment_post=Post.objects.filter(ID=post_id)[0], comment_parent=parent_id).order_by('-comment_date').prefetch_related()
    for c in comments:
        c.user = setup_current_user(c.user_id)
        c.child_comments = Comment.objects.none()
    return comments

def getgrandchildcomments(post_id, comments):
    if len(comments) == 0:
        return Comment.objects.none()
    else:
        for comment in comments:
            comment.user = setup_current_user(comment.user_id)
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(post_id, comment.comment_ID)
            return getgrandchildcomments(post_id, comment.child_comments)

def loadmorecomments(request):
    try:
        offset = int(request.GET["offset"])
        limit = int(request.GET["limit"])
        post_id = int(request.GET["post_id"])
        parent_id = int(request.GET["parent_id"])
        padding = int(request.GET["padding"])
        comments = Comment.objects.filter(comment_post=Post.objects.filter(ID=post_id)[0], comment_parent=parent_id).order_by('-comment_date').prefetch_related()
        comments = comments[offset:(offset + limit)]
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        for comment in comments:
            comment.user = setup_current_user(comment.user.ID)
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(post_id, comment.comment_ID)
            getgrandchildcomments(post_id, comment.child_comments)
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")
    return render(request, 'posts/comments/comment_list.html', {'comments':comments, 'padding':padding, 'word_list':word_list})

@csrf_exempt
def loadmoreprofileposts(request):
    try:
        offset = int(request.POST["offset"])
        limit = int(request.POST["limit"])
        user_id = int(request.POST["user_id"])
        fltr = request.POST["filter"]
        hasMore = "True"
        if fltr == "all" or fltr == "":
            moreposts = Post.objects.filter(post_author=user_id, post_status__in=["publish", "repost"], post_type__in=["post","quiz","media","link","questions","answer","repost"]).order_by('-post_date')
            if moreposts.count() <= offset :
                moreposts = moreposts[offset:]
                hasMore = "False"
            elif moreposts.count() <= offset + limit:
                moreposts = moreposts[offset:]
                hasMore = "False"
            else:
                moreposts = moreposts[offset:(offset + limit)]
        else:
            if fltr == "question":
                fltr = "questions"
            moreposts = Post.objects.filter(post_author=user_id, post_status="publish", post_type=fltr).order_by('-post_date')
            if moreposts.count() <= offset :
                moreposts = moreposts[offset:]
                hasMore = "False"
            elif moreposts.count() <= offset + limit:
                moreposts = moreposts[offset:]
                hasMore = "False"
            else:
                moreposts = moreposts[offset:(offset + limit)]
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        for post in moreposts:
            setup_postmeta(post, word_list)
            if post.post_type == "link":
                post.photo_from_url = fun.get_photo_from_url(post.post_content)
            elif post.post_type == "media":
                setup_mediameta(post)
            elif post.post_type == "quiz":
                post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
                post.post_title = post.post_title.replace(" - Sosyorol", "")
                if post.quiz_type == "media":
                    setup_media_quizmeta(post, word_list)
                elif post.quiz_type == "colorBox":
                    setup_colorbox_quizmeta(post, word_list)
                else:
                    setup_quizmeta(post, word_list)
            elif post.post_type == "repost":
                post.parent = Post.objects.filter(ID=post.post_parent)[0]
                setup_postmeta(post.parent, word_list)
                if post.parent.post_type == "link":
                    post.parent.photo_from_url = fun.get_photo_from_url(post.parent.post_content)
                elif post.parent.post_type == "media":
                    setup_mediameta(post.parent)
                elif post.parent.post_type == "quiz":
                    post.parent.quiz_type = PostMeta.objects.filter(post_id=post.parent.ID, meta_key="quiz_type")[0].meta_value
                    post.parent.post_title = post.parent.post_title.replace(" - Sosyorol", "")
                    if post.parent.quiz_type == "media":
                        setup_media_quizmeta(post.parent, word_list)
                    elif post.parent.quiz_type == "colorBox":
                        setup_colorbox_quizmeta(post.parent, word_list)
                    else:
                        setup_quizmeta(post.parent, word_list)
                post.parent.comments = Comment.objects.filter(comment_post=post.parent, comment_parent=0).order_by('-comment_date').prefetch_related()
                post.parent.comments = post.parent.comments[:5]
                for comment in post.parent.comments:
                    comment.user = setup_current_user(comment.user.ID)
                    comment.child_comments = Comment.objects.none()
                    comment.child_comments = getchildcomments(post.parent.ID, comment.comment_ID)
                    getgrandchildcomments(post.parent.ID, comment.child_comments)
            post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
            post.comments = post.comments[:5]
            for comment in post.comments:
                comment.user = setup_current_user(comment.user.ID)
                comment.child_comments = Comment.objects.none()
                comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
                getgrandchildcomments(post.ID, comment.child_comments)
        if fltr == "questions":
            fltr = "question"
        return render(request, 'posts/loadmoreposts.html', {'moreposts':moreposts, 'word_list':word_list, 'fltr':fltr, 'offset':offset, 'hasMore':hasMore, 'current_user':current_user})
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")

@csrf_exempt
def loadmorecommunityposts(request):
    print("test")
    try:
        offset = int(request.POST["offset"])
        limit = int(request.POST["limit"])
        fltr = request.POST["filter"]
        term_id = int(request.POST["term_id"])
        print(term_id, offset, limit)
        community = Community.objects.filter(term_id=term_id)[0]
        taxonomy = TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
        post_ids = TermRelationship.objects.filter(term_taxonomy_id=taxonomy)
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        hasMore = "True"
        if fltr == "all" or fltr == "":
            moreposts = Post.objects.filter(ID__in=post_ids).order_by('-post_date')
            if moreposts.count() <= offset :
                moreposts = moreposts[offset:]
                hasMore = "False"
            elif moreposts.count() <= offset + limit:
                moreposts = moreposts[offset:]
                hasMore = "False"
            else:
                moreposts = moreposts[offset:(offset + limit)]
        else:
            if fltr == "question":
                fltr = "questions"
            moreposts = Post.objects.filter(ID__in=post_ids, post_type=fltr).order_by('-post_date')
            if moreposts.count() <= offset :
                moreposts = moreposts[offset:]
                hasMore = "False"
            elif moreposts.count() <= offset + limit:
                moreposts = moreposts[offset:]
                hasMore = "False"
            else:
                moreposts = moreposts[offset:(offset + limit)]
        if current_uid != -1 and current_uid != None:
            current_user = setup_current_user(current_uid)
            lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        else:
            current_user = None
            lang = "en-EN"
        word_list = Languages.objects.filter(Q(lang_code = lang))
        print(moreposts)
        for post in moreposts:
            setup_postmeta(post, word_list)
            if post.post_type == "link":
                post.photo_from_url = fun.get_photo_from_url(post.post_content)
            elif post.post_type == "media":
                setup_mediameta(post)
            elif post.post_type == "poll":
                setup_pollmeta(post, word_list)
            elif post.post_type == "quiz":
                post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
                post.post_title = post.post_title.replace(" - Sosyorol", "")
                if post.quiz_type == "media":
                    setup_media_quizmeta(post, word_list)
                elif post.quiz_type == "colorBox":
                    setup_colorbox_quizmeta(post, word_list)
                else:
                    setup_quizmeta(post, word_list)
            post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
            post.comments = post.comments[:5]
            for comment in post.comments:
                comment.user = setup_current_user(comment.user.ID)
                comment.child_comments = Comment.objects.none()
                comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
                getgrandchildcomments(post.ID, comment.child_comments)
        if fltr == "questions":
            fltr = "question"
        return render(request, 'posts/loadmoreposts.html', {'moreposts':moreposts, 'word_list':word_list, 'fltr':fltr, 'offset':offset, 'hasMore':hasMore, 'current_user':current_user})
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")

@csrf_exempt
def loadmorehomeposts(request):
    offset = int(request.POST["offset"])
    limit = int(request.POST["limit"])
    fltr = "all"
    hasMore = "True"
    #cache_key = 'home_posts_'+str(offset)+'_'+str(offset+limit) # needs to be unique
    #cache_time = 300 # time in seconds for cache to be valid
    #moreposts = cache.get(cache_key) # returns None if no key-value pair
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(lang_code = lang)
    #if not moreposts:
    if True:
        moreposts, hasMore = get_feed_posts(offset, limit)
        for post in moreposts:
            setup_postmeta(post, word_list)
            if post.post_type == "link":
                post.photo_from_url = fun.get_photo_from_url(post.post_content)
            elif post.post_type == "media":
                setup_mediameta(post)
            elif post.post_type == "poll":
                setup_pollmeta(post, word_list)
            elif post.post_type == "quiz":
                post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
                post.post_title = post.post_title.replace(" - Sosyorol", "")
                if post.quiz_type == "media":
                    setup_media_quizmeta(post, word_list)
                elif post.quiz_type == "colorBox":
                    setup_colorbox_quizmeta(post, word_list)
                else:
                    setup_quizmeta(post, word_list)
            post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
            post.comments = post.comments[:5]
            for comment in post.comments:
                comment.user = setup_current_user(comment.user.ID)
                comment.child_comments = Comment.objects.none()
                comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
                getgrandchildcomments(post.ID, comment.child_comments)
    #cache.set(cache_key, moreposts, cache_time)
    return render(request, 'posts/loadmoreposts.html', {'moreposts':moreposts, 'word_list':word_list, 'fltr':fltr, 'offset':offset, 'hasMore':hasMore, 'current_user':current_user})

@csrf_exempt
def loadmorehistoryposts(request):
    try:
        import re
        offset = int(request.POST["offset"])
        limit = int(request.POST["limit"])
        fltr = request.POST["filter"]
        hasMore = "True"
        query = request.POST["query"]
        if query is None:
            query = ""
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'language')[0].meta_value
        word_list = Languages.objects.filter(lang_code = lang)
        search_history = SearchHistory.objects.filter(user_id=current_uid).filter(is_deleted=0).filter(search_term__icontains=query)
        post_history = PostHistory.objects.filter(user_id=current_uid).filter(is_deleted=0)
        for p in post_history:
            if fltr == "all" or fltr == p.post.post_type:
                setup_postmeta(p.post, word_list)
                if p.post.post_type == "media":
                    setup_mediameta(p.post)
                elif p.post.post_type == "poll":
                    setup_pollmeta(p.post, word_list)
                elif p.post.post_type == "link":
                    p.post.photo_from_url = fun.get_photo_from_url(p.post.post_content)
                elif p.post.post_type == "questions":
                    p.post.isanswered = isquestionanswered(p.post, current_uid)
                    p.post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=p.post.ID)
                    for answer in p.post.answers:
                        setup_postmeta(answer, word_list)
                elif p.post.post_type == "quiz":
                    p.post.quiz_type = PostMeta.objects.filter(post_id=p.post.ID, meta_key="quiz_type")[0].meta_value
                    p.post.post_title = p.post.post_title.replace(" - Sosyorol", "")
                    setup_postmeta(p.post, word_list)
                    if p.post.quiz_type == "media":
                        setup_media_quizmeta(p.post, word_list)
                    elif p.post.quiz_type == "colorBox":
                        setup_colorbox_quizmeta(p.post, word_list)
                    else:
                        setup_quizmeta(p.post, word_list)
                p.post.comments = Comment.objects.filter(comment_post=p.post, comment_parent=0).order_by('-comment_date').prefetch_related()
                p.post.comments = p.post.comments[:5]
                for comment in p.post.comments:
                    comment.user = setup_current_user(comment.user.ID)
                    comment.child_comments = Comment.objects.none()
                    comment.child_comments = getchildcomments(p.post.ID, comment.comment_ID)
                    getgrandchildcomments(p.post.ID, comment.child_comments)

        community_history = CommunityHistory.objects.filter(user_id=current_uid).filter(is_deleted=0)
        for c in community_history:
            follower_ids = FollowedCommunities.objects.filter(term=c.term)
            follower_ids = list({x.user_id: x for x in follower_ids}.keys())
            c.term.followers = User.objects.filter(ID__in=follower_ids)
                
        user_history = UserHistory.objects.filter(user_id=current_uid).filter(is_deleted=0)
        for user in user_history:
            user_desc = UserMeta.objects.filter(user_id = user.visited_user.ID).filter(meta_key = 'description')[0]
            user.visited_user.set_description(user_desc.meta_value)
            avatar_url = UserMeta.objects.filter(user=user.visited_user, meta_key="avatar_url")[0].meta_value
            user.visited_user.set_avatar(avatar_url)
        
        history = sorted(chain(search_history, post_history, community_history, user_history), key=lambda instance: instance.date, reverse=True)
        history_groups = {}
        for h in history:
            dict_key = h.date
            #locale.setlocale(locale.LC_TIME, lang.replace("-","_"))
            dict_key = dt.datetime.strftime(dict_key.date(), '%d %B %Y')
            if dict_key in history_groups:
                if h.history_type == "post":
                    if re.search(query, h.post.post_title, re.IGNORECASE):
                        history_groups[dict_key].append(h)
                elif h.history_type == "community":
                    if re.search(query, h.term.name, re.IGNORECASE):
                        history_groups[dict_key].append(h)
                elif h.history_type == "profile":
                    if re.search(query, h.visited_user.display_name, re.IGNORECASE) or re.search(query, h.visited_user.user_login, re.IGNORECASE):
                        history_groups[dict_key].append(h)
                else:
                    history_groups[dict_key].append(h)
            else:
                if fltr == "all" or fltr == h.history_type:
                    if h.history_type == "post":
                        if re.search(query, h.post.post_title, re.IGNORECASE):
                            history_groups[dict_key] = [h]
                    elif h.history_type == "community":
                        if re.search(query, h.term.name, re.IGNORECASE):
                            history_groups[dict_key] = [h]
                    elif h.history_type == "profile":
                        if re.search(query, h.visited_user.display_name, re.IGNORECASE) or re.search(query, h.visited_user.user_login, re.IGNORECASE):
                            history_groups[dict_key] = [h]
                    else:
                        history_groups[dict_key] = [h]
        if offset+limit >= len(list(history_groups.keys())):
            hasMore = "False"
        history_groups = {k: history_groups[k] for k in list(history_groups.keys())[offset:offset+limit]}
        return render(request, "includes/historyfeed.html", {'filter':fltr, 'history':history_groups, 'query':query, 'word_list':word_list, 'fltr':fltr, 'offset':offset, 'hasMore':hasMore, 'current_user':current_user})
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")

def  get_answered_questions_comms(user_id):
    answers = Post.objects.filter(post_author=user_id, post_status="publish", post_type="answer")
    communities = []
    for answer in answers:
        community_taxonomy_ids = TermRelationship.objects.filter(object_id=answer.post_parent)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        communities.extend(community_ids)
    return communities

def get_community_questions(communities, limit=None):
    taxonomies = TermTaxonomy.objects.filter(term_id__in=communities)
    post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomies)
    post_ids = list({x.object_id: x for x in post_ids}.keys())
    questions = Post.objects.filter(ID__in=post_ids, post_type="questions").order_by('-post_date')
    if limit != None:
        questions = questions[:limit]
    return questions

def is_question_answered(question_id, user_id):
    answers = Post.objects.filter(post_author=user_id, post_type="answer", post_status="publish", post_parent=question_id)
    if answers.count() > 0:
        return True
    return False

def get_suggested_questions(current_uid):
    communities = get_answered_questions_comms(current_uid)
    questions = get_community_questions(communities)
    suggested = []
    for question in questions:
        if question.post_author != current_uid:
            if is_question_answered(question.ID, current_uid) == False:
                if question not in suggested:
                    suggested.append(question)
    if len(suggested) > 10:
        suggested = suggested[:10]
    elif len(suggested) < 10:
        followed_communities = FollowedCommunities.objects.filter(user_id = current_uid).order_by('-date').prefetch_related()
        followed_communities = list({x.term_id: x for x in followed_communities}.keys())
        questions = get_community_questions(followed_communities, (10 - len(suggested)))
        for question in questions:
            if question.post_author != current_uid:
                if is_question_answered(question.ID, current_uid) == False:
                    if question not in suggested:
                        suggested.append(question)
        ## TODO: Eğer en az 10 suggested yok ise görüntülediğim toplulukların sorularını ekle
        if len(suggested) < 10:
            community_history = CommunityHistory.objects.filter(user_id=current_uid).order_by("-counter")
            community_history_ids = list({x.term_id: x for x in community_history}.keys())
            questions = get_community_questions(community_history_ids)
            for question in questions:
                if question.post_author != current_uid:
                    if is_question_answered(question.ID, current_uid) == False:
                        if question not in suggested:
                            suggested.append(question)
            if len(suggested) > 10:
                suggested = suggested[:10]
            elif len(suggested) < 10:
                posts = (PostHistory.objects.values('post_id').annotate(dcount=Count('post_id')).order_by())
                for p in posts:
                    question = Post.objects.filter(ID=p["post_id"])[0]
                    if question.post_type == "questions":
                        if question.post_author != current_uid:
                            if is_question_answered(question.ID, current_uid) == False:
                                if question not in suggested:
                                    suggested.append(question)
                    if len(suggested) == 10:
                        break
    return suggested

def is_user_following(follower_id, following_id):
    follow = UserRelation.objects.filter(follower_id=follower_id, following_id=following_id)
    if follow.count() > 0:
        return True
    return False

def get_suggested_users2(current_uid):
    followings = UserRelation.objects.filter(follower_id=current_uid)
    followings = list({x.following_id: x for x in followings}.keys())
    followings_followings = UserRelation.objects.filter(follower_id__in=followings)
    users = []
    for f in followings_followings:
        try:
            if is_user_following(current_uid, f.following_id) == False and f.following_id != current_uid:
                if f.following not in users:
                    users.append(f.following)
        except:
            pass
    if len(users) > 10:
        users = users[:10]
    elif len(users) < 10:
        user_history = (UserHistory.objects.values('user_id').annotate(dcount=Count('user_id')).order_by())
        for p in user_history:
            u = User.objects.filter(ID=p["user_id"])[0]
            try:
                if is_user_following(current_uid, u.ID) == False and u.ID != current_uid:
                    if u not in users:
                        users.append(u)
            except:
                pass
            if len(users) == 10:
                break
    ## TODO: if len(users) < 10, then add popular users like celebrities
    return users

def does_user_follow_community(user_id, community_id):
    comm = FollowedCommunities.objects.filter(user_id=user_id, term_id=community_id)
    if comm.count() > 0:
        return True
    return False

def get_suggested_communities(current_uid, return_all=False):
    community_history = CommunityHistory.objects.filter(user_id=current_uid).order_by("-counter")
    suggested = []
    for ch in community_history:
        if does_user_follow_community(current_uid, ch.term_id) == False:
            if ch.term not in suggested:
                suggested.append(ch.term)
    if len(suggested) > 10 and not return_all:
        suggested = suggested[:10]
    elif len(suggested) < 10:
        communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:(10 - len(suggested))].prefetch_related()
        for c in communities:
            if does_user_follow_community(current_uid, c.term_id) == False:
                if c.term not in suggested:
                    suggested.append(c.term)
    return suggested

def get_suggested_users(word_list, current_user):
    suggesteds = []
    visitor_followings_ids = list({x.following_id: x for x in current_user.followings}.keys())
    suggestion_dict = dict()
    for vid in visitor_followings_ids:
        followings = UserRelation.objects.filter(follower_id=vid)
        followings_ids = list({x.following_id: x for x in followings}.keys())
        for fid in followings_ids:
            if fid in suggestion_dict:
                suggestion_dict[fid] = suggestion_dict[fid] + 1
            else:
                suggestion_dict[fid] = 1
    for (k, _) in suggestion_dict.items():
        isFollowed = UserRelation.objects.filter(following_id=k, follower=current_user)
        if isFollowed.count() == 0 and k != current_user.ID and k != current_user.ID:
            try:
                user = setup_current_user(k)
                if user not in suggesteds:
                    suggesteds.append(user)
            except:
                pass
    for suggested in suggesteds:
        relative_users = UserRelation.objects.filter(following=suggested, follower_id__in=visitor_followings_ids)
        relative_usernames = list({"u/"+x.follower.user_login: x for x in relative_users}.keys())
        and_string = word_list.filter(var_name="and")[0].translation
        people_string = ""
        if len(relative_usernames) == 1:
            people_string = relative_usernames[0]
        elif len(relative_usernames) == 2:
            people_string = relative_usernames[0] + " " + and_string + " " + relative_usernames[1]
        else:
            people_string = ", ".join(relative_usernames[0:2]) + " " + and_string + " " + str(len(relative_usernames) - 2) + " " + word_list.filter(var_name="more-users")[0].translation
        suggested.relatives = word_list.filter(var_name="relative_followers_string")[0].translation.replace("{user}", people_string)
    return suggesteds
"""
epoch = dt.datetime(1970, 1, 1)

def epoch_seconds(date):
    td = date.replace(tzinfo=None) - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
    return ups - downs

def hot(post):
    post_ratings = PostRating.objects.filter(post=post)
    ups = post_ratings.filter(opinion="like").count()
    downs = post_ratings.filter(opinion="dislike").count()
    return _hot(ups, downs, epoch_seconds(post.post_date))

def _hot(ups, downs, date):
    s = score(ups, downs)
    order = math.log10(max(abs(s), 1))
    if s > 0:
        sign = 1
    elif s < 0:
        sign = -1
    else:
        sign = 0
    seconds = date - 1544462791000
    return round(sign * order + seconds / 45000, 7)
"""
def get_seen_posts(user_id):
    seen_post_ids = PostHistory.objects.filter(user_id=user_id)
    seen_post_ids = list({x.post_id: x for x in seen_post_ids}.keys())
    return seen_post_ids

def posts_from_followed_communities(user_id):
    followed_communities = FollowedCommunities.objects.filter(user_id = user_id, is_active=1).order_by('-date').prefetch_related()
    followed_communities = list({x.term_id: x for x in followed_communities}.keys())
    taxonomies = TermTaxonomy.objects.filter(term_id__in=followed_communities)
    post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomies)
    post_ids = list({x.object_id: x for x in post_ids}.keys())
    return post_ids

def posts_upvoted_by_followings(user_id):
    followings = UserRelation.objects.filter(follower_id=user_id)
    followings = list({x.following_id: x for x in followings}.keys())
    upvoted_posts = PostRating.objects.filter(opinion="like", user_id__in=followings)
    upvoted_posts = list({x.post_id: x for x in upvoted_posts}.keys())
    return upvoted_posts

def posts_commented_by_followings(user_id):
    followings = UserRelation.objects.filter(follower_id=user_id)
    followings = list({x.following_id: x for x in followings}.keys())
    commented_posts = Comment.objects.filter(user_id__in=followings)
    commented_posts = list({x.comment_post.ID: x for x in commented_posts}.keys())
    return commented_posts

def posts_by_followings(user_id):
    followings = UserRelation.objects.filter(follower_id=user_id)
    followings = list({x.following_id: x for x in followings}.keys())
    posts = Post.objects.filter(author_id__in=followings)
    posts = list({x.ID: x for x in posts}.keys())
    return posts

def get_more_posts(posts, offset, limit):
    if len(posts) <= offset:
        posts = []
    elif len(posts) < (offset+limit):
        posts = posts[offset:]
    else:
        posts = posts[offset:(offset+limit)]
    return posts

def posts_from_communities(community_ids):
    taxonomies = TermTaxonomy.objects.filter(term_id__in=community_ids)
    taxonomy_ids = list({x.term_taxonomy_id: x for x in taxonomies}.keys())
    posts = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomy_ids)
    post_ids = list({x.object_id: x for x in posts}.keys())
    return post_ids

def get_feed_posts(offset, limit, step=1):
    has_more = "True"
    results = []
    posts = Post.objects.all()
    if step == 1:
        # The posts which are unseen and published in followed communities
        seen_post_ids = get_seen_posts(current_uid)
        post_ids = posts_from_followed_communities(current_uid)
        posts = posts.filter(ID__in=post_ids, post_status="publish", post_type__in=["post", "quiz", "poll", "answer", "link", "media"]).exclude(ID__in=seen_post_ids).exclude(post_author=current_uid).order_by("-post_date").prefetch_related()
        results = list(posts)
    
    if step == 1 and len(results) < (offset + limit):
        step = 2

    if step == 2:
        # The posts written by the followings
        post_ids = posts_by_followings(current_uid)
        moreresults = posts.filter(ID__in=post_ids).prefetch_related()
        if moreresults.count() > 0:
            moreresults = [x for x in moreresults if x not in results]
            results += moreresults
    
    if step == 2 and len(results) < (offset + limit):
        step = 3

    if step == 3:        
        # The posts upvoted by the followings
        post_ids = posts_upvoted_by_followings(current_uid)
        moreresults = posts.filter(ID__in=post_ids).prefetch_related()
        if moreresults.count() > 0:
            moreresults = [x for x in moreresults if x not in results]
            results += moreresults
    
    if step == 3 and len(results) < (offset + limit):
        step = 4

    if step == 4:           
        # The posts commented by the followings
        post_ids = posts_commented_by_followings(current_uid)
        moreresults = posts.filter(ID__in=post_ids).prefetch_related()
        if moreresults.count() > 0:
            moreresults = [x for x in moreresults if x not in results]
            results += moreresults

    if step == 4 and len(results) < (offset + limit):
        step = 5

    if step == 5:   
        # The posts published in suggested communities
        suggested_communities = get_suggested_communities(current_uid, return_all=True)
        suggested_communities = list({x.term_id: x for x in suggested_communities}.keys())
        post_ids = posts_from_communities(suggested_communities)
        print(post_ids)
        moreresults = Post.objects.filter(ID__in=post_ids).prefetch_related()
        print(moreresults)
        if moreresults.count() > 0:
            moreresults = [x for x in moreresults if x not in results]
            results += moreresults

    if step == 5 and len(results) < (offset + limit):
        has_more = "False"

    return get_more_posts(results, offset, limit), has_more

'''---------------------------------------
  OPERATIONS              
-----------------------------------------'''
@csrf_exempt
def createdbuser(request):
    import bcrypt
    max_user = User.objects.all().order_by("-ID")[0]
    max_id = max_user.ID + 1
    email = request.POST["email"]
    user_login = request.POST["user_login"]
    user_pass = bytes(request.POST["user_password"], encoding='utf-8')
    display_name = request.POST["display_name"]
    new_user = User(ID=max_id, user_login=user_login, user_pass=bcrypt.hashpw(user_pass, bcrypt.gensalt()), user_nicename=user_login, user_email=email, display_name=display_name, user_registered=dt.datetime.now())
    new_user.save()
    new_user = User.objects.filter(user_email=email)[0]
    print(new_user.ID)
    new_lang = UserMeta(user_id=new_user.ID, meta_key="language", meta_value="en-EN")
    new_lang.save()
    new_mode = UserMeta(user_id=new_user.ID, meta_key="mode", meta_value="light")
    new_mode.save()
    request.COOKIES["uid"] = "sosyoroluseruid"+str(new_user.ID)
    return HttpResponseRedirect("/")

@csrf_exempt
def changemode(request):
    mode = request.POST["mode"]
    user_id = int(request.POST["uid"])
    print(user_id, mode)
    usermeta = UserMeta.objects.filter(user_id=user_id, meta_key="mode")
    if usermeta.count() > 0:
        usermeta = usermeta[0]
        usermeta.meta_value = mode
        usermeta.save()
    else:
        usermeta = UserMeta(user_id=user_id, meta_key="mode", meta_value=mode)
        usermeta.save()
    return JsonResponse({})

def votepoll(request):
    post_id = int(request.POST["post_id"])
    user_id = current_uid
    lang = UserMeta.objects.filter(user_id = current_uid, meta_key = 'language')[0].meta_value
    word_list = Languages.objects.filter(lang_code = lang)
    choice = request.POST["option"]
    comment = ""
    new_vote = SossyComments(post_id=post_id, user_id=user_id, choice=choice, comment=comment)
    new_vote.save()
    html_string = " <div class='bsbb full-width'>"
    poll = Post.objects.filter(Q(ID=post_id))[0]
    setup_postmeta(poll,word_list)
    setup_pollmeta(poll, word_list)
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
    from sosyorol.forms import MediaFileUploadForm
    form = MediaFileUploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        photo = form.save()
        form = MediaFileUploadForm()
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)

@csrf_exempt
def changeprofilepicture(request):
    from sosyorol.forms import MediaFileUploadForm
    form = MediaFileUploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        photo = form.save()
        form = MediaFileUploadForm()
        new_cred = UserMeta.objects.filter(user_id=current_uid, meta_key="avatar_url")[0]
        new_cred.meta_value = photo.file.url
        new_cred.save()
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        msg = fun.ucfirst(word_list.filter(var_name="picture-has-changed")[0].translation)
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url, 'msg': msg}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)

@csrf_exempt
def uploadmediagetcolor(request):
    from sosyorol.forms import MediaFileUploadForm
    from colorthief import ColorThief
    form = MediaFileUploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        photo = form.save()
        form = MediaFileUploadForm()
        color_thief = ColorThief("static/assets/"+photo.file.name)
        dominant_color = color_thief.get_color(quality=1)
        (r, g, b) = dominant_color
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url, 'color': 'rgb('+str(r)+','+str(g)+','+str(b)+')'}
    else:
        data = {'is_valid': False}
    return HttpResponse(json.dumps(data),content_type="application/json")

def savenewlist(request):
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
            print(post_id)
            print(user_id)
            print("saved")
        elif operation == "remove":
            instance = SavedPosts.objects.get(post_id=post_id, user_id=user_id)
            instance.delete()
        return HttpResponseRedirect(redirect)
    except:
        print("pass")
        return HttpResponseRedirect("")

def savenewcommunity(request):
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

@csrf_exempt
def get_search_results(request):
    search_key = request.POST["search"]
    response_data = {}
    results = Community.objects.filter(Q(name__icontains=search_key))[:6]
    result_count = len(results)
    for result in results:
        response_data[result.slug] = "community!:!" + result.profile_img_small + "!:!" + result.name
    if (result_count < 6):
        diff = 6 - result_count
        results = Post.objects.filter(post_status="publish").filter(post_title__icontains=search_key).order_by('-post_date')[:diff]
        result_count += len(results)
        for result in results:
            result.hex_id = hex(result.ID + 100000).replace("x", "s")
            result.post_title = result.post_title.replace(" - Sosyorol", "")
            result.guid = arrange_post_slug(result.post_title)
            result.author = setup_current_user(result.post_author)
            url = "u/"+result.author.user_login+"/"+result.hex_id+"/"+result.guid
            response_data[url] = "post!:!" +result.post_title
    if (result_count < 6):
        diff = 6 - result_count
        results = User.objects.filter(Q(display_name__icontains=search_key))[:diff]
        for result in results:
            result = setup_current_user(result.ID)
            response_data[result.user_nicename] = "user!:!" + result.avatar_url + "!:!" + result.user_login
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def getlanguages(request):
    search_key = request.GET["search"]
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    response_data = {}
    results = Languages.objects.filter(lang_code=lang, var_name__icontains="lang-ns-", translation__icontains=search_key)
    for result in results:
        response_data[result.var_name] = "lang!:!" +result.translation
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def updatelanguage(request):
    new_lang_key = request.POST["lang"]
    print(new_lang_key)
    old_lang = UserMeta.objects.filter(user_id=current_uid, meta_key="language")
    if old_lang.count() > 0:
        old_lang = old_lang[0]
        old_lang.meta_value = new_lang_key
        old_lang.save()
    else:
        new_lang = UserMeta(user_id=current_uid, meta_key="language", meta_value=new_lang_key)
        new_lang.save()
    #cache_key = 'current_user_lang'
    #cache_time = 86400
    #cache.clear()
    #cache.set(cache_key, new_lang_key, cache_time)
    return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def savenewquiz(request):
    import re
    quiz_title = request.POST["quiz_title"]
    quiz_desc = request.POST["quiz_desc"]
    results = json.loads(request.POST['results'])
    quiz_type = request.POST["questionType"]
    communities = json.loads(request.POST['communities'])
    questions = json.loads(request.POST['questions'])
    
    flairs = json.loads(request.POST['flairs'])

    post_excerpt = re.sub("(<img.*?>)", "", quiz_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    post_excerpt = fun.striphtml(post_excerpt).replace('\n', '').rstrip()
    
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    solveXQuiz = word_list.get(var_name = 'solve-x-quiz').translation
    solveXQuiz = solveXQuiz.replace("quiz_name", quiz_title)
    solveXQuiz = fun.ucfirst(solveXQuiz)
    if len(post_excerpt) < 106:
        post_excerpt = post_excerpt+" "+solveXQuiz
    
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content=quiz_desc, post_date=dt.datetime.now(), author=current_user, post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="quiz", post_excerpt=post_excerpt, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]
    new_quiz_type = PostMeta(post_id=new_quiz.ID, meta_key="quiz_type", meta_value=quiz_type)
    new_quiz_type.save()

    response_data = {}
    for follower in current_user.followers:
        new_quiz.hex_id = hex(new_quiz.ID + 100000).replace("x", "s")
        new_quiz.guid = arrange_post_slug(new_quiz.post_title)
        url = "/u/"+current_user.user_login+"/"+new_quiz.hex_id+"/"+new_quiz.guid
        response_data['url'] = url
        new_notification = Notification(date=dt.datetime.now(), url=url, notification_variable="new-post", 
                                        seen=0, from_u_id=current_uid, to_u=follower.follower_id, related_obj=new_quiz.ID)
        new_notification.save()

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.filter(term=term)[0]
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()
        followers = FollowedCommunities.objects.filter(term=term)
        for follower in followers:
            if(follower.user != current_user):
                new_notification = Notification(date=dt.datetime.now(), url="/c/"+term.slug, notification_variable="community-post", 
                                                seen=0, from_u_id=-1, to_u=follower.user_id, related_obj=term.term_id)
                new_notification.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.filter(name=tokens[1])[0]
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()
    
    resultCounter = 1
    for (k, v) in results.items():
        result_text = "<h2>"+str(v["title"])+"</h2><br>"+str(v["desc"])
        result_img = str(v["img"])
        new_result_text = PostMeta(post_id=new_quiz.ID, meta_key="test_sonuc_"+str(resultCounter)+"_result_text", meta_value=result_text)
        new_result_text.save()
        new_result_img = PostMeta(post_id=new_quiz.ID, meta_key="test_sonuc_"+str(resultCounter)+"_result_img", meta_value=result_img)
        new_result_img.save()
        resultCounter += 1
    new_result_number = PostMeta(post_id=new_quiz.ID, meta_key="result_number", meta_value=(resultCounter - 1))
    new_result_number.save()
    
    questionCounter = 1
    for (k, v) in questions.items():
        question_text = str(v["question"])
        new_question_text = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_question", meta_value=question_text)
        new_question_text.save()
        if quiz_type == "media":
            question_img = str(v["img"])
            new_question_img = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_img", meta_value=question_img)
            new_question_img.save()
        elif quiz_type == "colorBox":
            question_color = str(v["color"])
            new_question_color = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_color", meta_value=question_color)
            new_question_color.save()
        answer_type = str(v["answerType"])
        new_answer_type = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_answer_type", meta_value=answer_type)
        new_answer_type.save()
        answerCounter = 1
        for (key, val) in v["answers"].items():
            answer_content = str(val["content"])
            new_answer_text = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_answer_"+str(answerCounter)+"_content", meta_value=answer_content)
            new_answer_text.save()
            assoc_result = str(val["assocResult"])
            new_answer_result = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_answer_"+str(answerCounter)+"_assoc_result", meta_value=assoc_result)
            new_answer_result.save()
            if answer_type == "colorBox":
                answer_color = str(val["color"])
                new_answer_color = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_answer_"+str(answerCounter)+"_color", meta_value=answer_color)
                new_answer_color.save()
            answerCounter += 1
        new_answer_number = PostMeta(post_id=new_quiz.ID, meta_key="soru_"+str(questionCounter)+"_answer_number", meta_value=(answerCounter - 1))
        new_answer_number.save()
        questionCounter += 1
    new_question_number = PostMeta(post_id=new_quiz.ID, meta_key="question_number", meta_value=(questionCounter - 1))
    new_question_number.save()                    
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewpost(request):
    import re
    quiz_title = request.POST["post_title"]
    quiz_desc = request.POST["post_content"]
    communities = json.loads(request.POST['communities'])
    flairs = json.loads(request.POST['flairs'])

    post_excerpt = re.sub("(<img.*?>)", "", quiz_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    post_excerpt = fun.striphtml(post_excerpt).replace('\n', '').rstrip()
    
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content=quiz_desc, post_date=dt.datetime.now(), author=current_user, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="post", post_excerpt=post_excerpt, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    response_data = {}
    for follower in current_user.followers:
        new_quiz.hex_id = hex(new_quiz.ID + 100000).replace("x", "s")
        new_quiz.guid = arrange_post_slug(new_quiz.post_title)
        url = "/u/"+current_user.user_login+"/"+new_quiz.hex_id+"/"+new_quiz.guid
        response_data["url"] = url
        new_notification = Notification(date=dt.datetime.now(), url=url, notification_variable="new-post", 
                                        seen=0, from_u_id=current_uid, to_u=follower.follower_id, related_obj=new_quiz.ID)
        new_notification.save()

    for (k, v) in communities.items():
        term = Community.objects.get(name=str(v))
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()
        followers = FollowedCommunities.objects.filter(term=term)
        for follower in followers:
            if(follower.user != current_user):
                new_notification = Notification(date=dt.datetime.now(), url="/c/"+term.slug, notification_variable="community-post", 
                                                seen=0, from_u_id=-1, to_u=follower.user_id, related_obj=term.term_id)
                new_notification.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()                       
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewmediapost(request):
    quiz_title = request.POST["post_title"]
    media_type = request.POST["media_type"]
    if media_type != "video":
        media_type = "image"
    media_url = request.POST["media_url"]
    communities = json.loads(request.POST['communities'])
    flairs = json.loads(request.POST['flairs'])
    
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content="", post_date=dt.datetime.now(), author=current_user, post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="media", post_excerpt=quiz_title, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    response_data = {}
    for follower in current_user.followers:
        new_quiz.hex_id = hex(new_quiz.ID + 100000).replace("x", "s")
        new_quiz.guid = arrange_post_slug(new_quiz.post_title)
        url = "/u/"+current_user.user_login+"/"+new_quiz.hex_id+"/"+new_quiz.guid
        response_data["url"] = url
        new_notification = Notification(date=dt.datetime.now(), url=url, notification_variable="new-post", 
                                        seen=0, from_u_id=current_uid, to_u_id=follower.follower_id, related_obj=new_quiz.ID)
        new_notification.save()

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()
        followers = FollowedCommunities.objects.filter(term=term)
        for follower in followers:
            if(follower.user_id != current_uid):
                new_notification = Notification(date=dt.datetime.now(), url="/c/"+term.slug, notification_variable="community-post", 
                                                seen=0, from_u_id=-1, to_u_id=follower.user_id, related_obj=term.term_id)
                new_notification.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()

    new_media_type = PostMeta(post_id=new_quiz.ID, meta_key="media_type", meta_value=media_type)
    new_media_type.save()

    new_media_url = PostMeta(post_id=new_quiz.ID, meta_key="media_url", meta_value=media_url)
    new_media_url.save()                 
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewlink(request):
    quiz_title = request.POST["post_title"]
    post_url = request.POST["post_url"]
    communities = json.loads(request.POST['communities'])
    flairs = json.loads(request.POST['flairs'])
    
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content="", post_date=dt.datetime.now(), author=current_user, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="link", post_excerpt=quiz_title, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    response_data = {}
    for follower in current_user.followers:
        new_quiz.hex_id = hex(new_quiz.ID + 100000).replace("x", "s")
        new_quiz.guid = arrange_post_slug(new_quiz.post_title)
        url = "/u/"+current_user.user_login+"/"+new_quiz.hex_id+"/"+new_quiz.guid
        response_data["url"] = url
        new_notification = Notification(date=dt.datetime.now(), url=url, notification_variable="new-post", 
                                        seen=0, from_u_id=current_uid, to_u=follower.follower_id, related_obj=new_quiz.ID)
        new_notification.save()

    for (k, v) in communities.items():
        term = Community.objects.get(name=str(v))
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()
        followers = FollowedCommunities.objects.filter(term=term)
        for follower in followers:
            if(follower.user != current_user):
                new_notification = Notification(date=dt.datetime.now(), url="/c/"+term.slug, notification_variable="community-post", 
                                                seen=0, from_u_id=-1, to_u=follower.user_id, related_obj=term.term_id)
                new_notification.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()

    post_url = PostMeta(post_id=new_quiz.ID, meta_key="post_url", meta_value=post_url)
    post_url.save()                
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewquestion(request):
    import re
    quiz_title = request.POST["post_title"]
    post_url = request.POST["post_url"]
    communities = json.loads(request.POST['communities'])
    flairs = json.loads(request.POST['flairs'])
    quiz_desc = request.POST["post_content"]

    post_excerpt = re.sub("(<img.*?>)", "", quiz_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    post_excerpt = fun.striphtml(post_excerpt).replace('\n', '').rstrip()
    
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content=quiz_desc, post_author=current_uid, post_date=dt.datetime.now(), author=current_user, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="questions", post_excerpt=post_excerpt, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    response_data = {}
    for follower in current_user.followers:
        new_quiz.hex_id = hex(new_quiz.ID + 100000).replace("x", "s")
        new_quiz.guid = arrange_post_slug(new_quiz.post_title)
        url = "/u/"+current_user.user_login+"/"+new_quiz.hex_id+"/"+new_quiz.guid
        response_data["url"] = url
        new_notification = Notification(date=dt.datetime.now(), url=url, notification_variable="new-post", 
                                        seen=0, from_u_id=current_uid, to_u_id=follower.follower_id, related_obj=new_quiz.ID)
        new_notification.save()

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()
        followers = FollowedCommunities.objects.filter(term=term)
        for follower in followers:
            if(follower.user != current_user):
                new_notification = Notification(date=dt.datetime.now(), url="/c/"+term.slug, notification_variable="community-post", 
                                                seen=0, from_u_id=-1, to_u_id=follower.user_id, related_obj=term.term_id)
                new_notification.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()

    post_url = PostMeta(post_id=new_quiz.ID, meta_key="post_url", meta_value=post_url)
    post_url.save()                  
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewpoll(request):
    import re
    quiz_title = request.POST["post_title"]
    communities = json.loads(request.POST['communities'])
    flairs = json.loads(request.POST['flairs'])
    options = json.loads(request.POST['poll_options'])
    quiz_desc = request.POST["post_content"]
    poll_duration = request.POST["poll_duration"]

    post_excerpt = re.sub("(<img.*?>)", "", quiz_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    post_excerpt = fun.striphtml(post_excerpt).replace('\n', '').rstrip()
    lang = UserMeta.objects.filter(user_id = current_uid, meta_key = 'language')[0].meta_value
    word_list = Languages.objects.filter(lang_code = lang)
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content=quiz_desc, post_date=dt.datetime.now(), author=current_user, post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="poll", post_excerpt=post_excerpt, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    response_data = {}
    for follower in current_user.followers:
        new_quiz.hex_id = hex(new_quiz.ID + 100000).replace("x", "s")
        new_quiz.guid = arrange_post_slug(new_quiz.post_title)
        url = "/u/"+current_user.user_login+"/"+new_quiz.hex_id+"/"+new_quiz.guid
        response_data["url"] = url
        new_notification = Notification(date=dt.datetime.now(), url=url, notification_variable="new-post", 
                                        seen=0, from_u_id=current_uid, to_u_id=follower.follower_id, related_obj=new_quiz.ID)
        new_notification.save()

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()
        followers = FollowedCommunities.objects.filter(term=term)
        for follower in followers:
            if(follower.user != current_user):
                new_notification = Notification(date=dt.datetime.now(), url="/c/"+term.slug, notification_variable="community-post", 
                                                seen=0, from_u_id=-1, to_u_id=follower.user_id, related_obj=term.term_id)
                new_notification.save()

    optionCounter = 1
    for (k, v) in options.items():
        new_poll_option = PostMeta(post_id=new_quiz.ID, meta_key="secenek_"+str(optionCounter), meta_value=str(v))
        new_poll_option.save()
        optionCounter = optionCounter + 1
    new_option_number = PostMeta(post_id=new_quiz.ID, meta_key="number_options", meta_value=(optionCounter - 1))
    new_option_number.save()

    new_poll_duration = PostMeta(post_id=new_quiz.ID, meta_key="poll_duration", meta_value=poll_duration)
    new_poll_duration.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()                
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savecomment(request):
    current_user = setup_current_user(current_uid)
    comment = request.POST["comment"]
    post_id = int(request.POST["post_id"])
    lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(lang_code = lang)
    post = Post.objects.filter(ID=post_id)[0]
    post = setup_postmeta(post, word_list)
    parent_id = int(request.POST["parent_id"])
    print(current_uid, post_id)
    new_comment = Comment(comment_approved=1, comment_author=current_user.display_name, comment_content=comment, comment_post_id=post_id, comment_parent=parent_id, comment_author_email=current_user.user_email, comment_date=dt.datetime.now(), user_id=current_uid)
    new_comment.save()
    new_comment = Comment.objects.filter(comment_author=current_user.display_name, comment_content=comment, comment_post_id=post_id, comment_parent=parent_id).order_by('-comment_date')[0]
    if parent_id > 0:
        comment = Comment.objects.get(comment_ID=parent_id)
        if(current_uid != comment.user_id):
            hex_id = hex(new_comment.comment_ID + 100000).replace("x", "c")
            url = "/u/"+current_user.user_login+"/comments/"+hex_id
            new_notification = Notification(notification_variable="comment-reply", seen=0, date=dt.datetime.now(), from_u_id=current_uid, to_u_id=comment.user_id, related_obj=new_comment.comment_ID, url=url)
            new_notification.save()
    else:
        post = Post.objects.get(ID=post_id)
        if(current_uid != post.post_author):
            hex_id = hex(new_comment.comment_ID + 100000).replace("x", "c")
            url = "/u/"+current_user.user_login+"/comments/"+hex_id
            new_notification = Notification(notification_variable="comment-on-post", seen=0, date=dt.datetime.now(), from_u_id=current_uid, to_u_id=post.post_author, related_obj=new_comment.comment_ID, url=url)
            new_notification.save()
    response_data = {}
    response_data['content'] = Languages.objects.filter(lang_code=lang, var_name="comment-saved-successfully")[0].translation
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewanswer(request):
    answer = request.POST["answer"]
    parent_id = int(request.POST["parent"])
    parent = Post.objects.filter(ID=parent_id)[0]
    current_user = setup_current_user(current_uid)
    new_answer = Post.objects.create(post_title=parent.post_title, post_content=answer, post_date=dt.datetime.now(), author=current_user, post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="answer", post_excerpt=parent.post_excerpt, post_parent=parent_id)
    #new_answer.save()
    new_answer = Post.objects.filter(post_title=parent.post_title, post_content=answer, post_date=dt.datetime.now(), author=current_user, post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="answer", post_excerpt=parent.post_excerpt, post_parent=parent_id)[0]
    response_data = {}
    if(current_uid != parent.post_author):
        print(new_answer.ID)
        new_answer.hex_id = hex(new_answer.ID + 100000).replace("x", "s")
        new_answer.guid = arrange_post_slug(new_answer.post_title)
        url = "/u/"+current_user.user_login+"/"+new_answer.hex_id+"/"+new_answer.guid
        response_data["url"] = url
        new_notification = Notification(notification_variable="answer-question", seen=0, from_u_id=current_uid, to_u_id= parent.post_author, date=dt.datetime.now(), url=url)
        new_notification.save()
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    response_data['content'] = Languages.objects.filter(lang_code=lang, var_name="answer-saved-successfully")[0].translation
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def getquizresult(request):
    try:
        selectedResult = int(request.POST["selectedResult"].replace("result",""))
        post_id = int(request.POST["quiz_id"])
        quiz_title = Post.objects.filter(ID=post_id)[0].post_title.replace(" - Sosyorol", "")
        result_obj = dict()
        result_obj["content"] = PostMeta.objects.filter(post_id=post_id, meta_key="test_sonuc_"+str(selectedResult)+"_result_text")[0].meta_value
        result_obj["img"] = PostMeta.objects.filter(post_id=post_id, meta_key="test_sonuc_"+str(selectedResult)+"_result_img")[0].meta_value
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")
    return render(request, 'posts/postdetails/quiz_result.html', {'result':result_obj, 'quiz_title':quiz_title, 'word_list':word_list})

def emloymentcredential(request):
    try:
        cred = UserMeta(user_id=current_uid, meta_key="employments", meta_value=json.dumps(request.GET))
        cred.save()
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'credential-saved-msg')[0].translation 
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 

def educationcredential(request):
    try:
        cred = UserMeta(user_id=current_uid, meta_key="educations", meta_value=json.dumps(request.GET))
        cred.save()
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'credential-saved-msg')[0].translation 
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
def locationcredential(request):
    try:
        cred = UserMeta(user_id=current_uid, meta_key="locations", meta_value=json.dumps(request.GET))
        cred.save()
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'credential-saved-msg')[0].translation 
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 

def languagecredential(request):
    try:
        cred = UserMeta(user_id=current_uid, meta_key="languages", meta_value=json.dumps(request.GET))
        cred.save()
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'credential-saved-msg')[0].translation 
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 

def editfullname(request):
    try:
        fullname = request.GET["fullname"]
        cred = User.objects.filter(ID=current_uid)[0]
        cred.display_name = fullname
        cred.save()
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'credential-saved-msg')[0].translation 
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 

def editprofiledesc(request):
    try:
        profiledesc = request.GET["profiledesc"]
        try:
            user_desc = UserMeta.objects.filter(user_id = current_uid, meta_key = 'description')[0]
            user_desc.meta_value = profiledesc
            user_desc.save()
        except:
            user_desc = UserMeta(user_id = current_uid, meta_key = 'description', meta_value=profiledesc)
            user_desc.save()
        return "success"
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 

def birthday(request):
    try:  
        birthday = request.GET["birthday"]
        birthdayobj = dt.datetime.strptime(birthday, '%d.%m.%Y')
        birthday = birthdayobj.strftime("%Y-%m-%d")
        cred = UserMeta(user_id=current_uid, meta_key="birthday", meta_value=birthday)
        cred.save()
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'credential-saved-msg')[0].translation 
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        return Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 

@csrf_exempt
def savenewusercredential(request):
    try:
        response_data = {}
        ctype = request.GET["type"]
        if ctype == "employment":
            response_data['content'] = emloymentcredential(request)
        elif ctype == "education":
            response_data['content'] = educationcredential(request)
        elif ctype == "location":
            response_data['content'] = locationcredential(request)
        elif ctype == "language":
            response_data['content'] = languagecredential(request)
        elif ctype == "fullname":
            response_data['content'] = editfullname(request)
        elif ctype == "profiledesc":
            response_data['content'] = editprofiledesc(request)
        elif ctype == "birthday":
            response_data['content'] = birthday(request)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def deleteusercredential(request):
    try:
        response_data = {}
        ID = request.GET["ID"]
        cred = UserMeta.objects.get(umeta_id=int(ID))
        cred.delete()
        response_data['content'] = "success"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def editusercredential(request):
    try:
        response_data = {}
        ID = request.GET["ID"]
        cred = UserMeta.objects.get(umeta_id=int(ID))
        if request.GET["type"] == "birthday":
            cred.meta_value = request.GET["birthday"]
        else:
            cred.meta_value = json.dumps(request.GET)
        cred.save()
        response_data['content'] = "success"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def followunfollowuser(request):
    try:
        response_data = {}
        op = request.GET["op"]
        followerId = int(request.GET["followerId"])
        followingId = int(request.GET["followingId"])
        lang = UserMeta.objects.filter(user_id=followerId, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(lang_code = lang)
        if(op == "follow"):
            new_rel = UserRelation(follower_id=followerId, following_id=followingId, date=dt.datetime.now())
            new_rel.save()
            follower = User.objects.get(ID=followerId)
            new_notification = Notification(date=dt.datetime.now(), url="/u/"+follower.user_login, notification_variable="follow", seen=0, from_u_id=followerId, to_u_id=followingId)
            new_notification.save()
            response_data['content'] = word_list.filter(var_name="user-followed-msg")[0].translation
        elif(op == "unfollow"):
            old_rel = UserRelation.objects.get(follower_id=followerId, following_id=followingId)
            old_rel.delete()
            response_data['content'] = word_list.filter(var_name="user-unfollowed-msg")[0].translation
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def removeprofilepicture(request):
    try:
        response_data = {}
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        cred = UserMeta.objects.filter(user_id=current_uid, meta_key="avatar_url")[0]
        cred.meta_value = avatar_url
        cred.save()
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        msg = fun.ucfirst(word_list.filter(var_name="picture-has-changed")[0].translation)
        response_data["msg"] = msg
        response_data["url"] = avatar_url
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def updatenotification(request):
    try:
        nid = int(request.POST["ID"])
        notif = Notification.objects.get(ID=nid)
        notif.seen = 1
        notif.save()
    except:
        pass
    return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def updateallnotifications(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    notifications = Notification.objects.filter(to_u_id=current_uid)
    lang = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'language')[0].meta_value
    word_list = Languages.objects.filter(lang_code = lang)
    notifs = dict()
    new_notifs = []
    old_notifs = []
    for n in notifications:
        n.opened = 1
        n.save()
        n.from_u = setup_current_user(n.from_u_id)
        n.date_diff = fun.humanizedate(n.date.replace(tzinfo=None), word_list, to=dt.datetime.now())
        n.notification = word_list.filter(var_name="notification-"+n.notification_variable)[0].translation
        n.notification = n.notification.replace("{user}", "<span class='fwbold'>u/"+n.from_u.user_login+"</span>")
        if n.date.day == dt.datetime.today().day and n.date.month == dt.datetime.today().month and n.date.year == dt.datetime.today().year:
            new_notifs.append(n)
        else:
            old_notifs.append(n)
    notifs["new"] = new_notifs
    notifs["earlier"] = old_notifs
    print(current_uid)
    print(notifs)
    return render(request, 'includes/general/notifications_popup.html', {'notifications':notifs, 'word_list':word_list})

@csrf_exempt
def followpost(request):
    response_data = {}
    try:
        post_id = request.POST["post_id"]
        operation = request.POST["op"]
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        if(operation == "follow"):
            new_follow = FollowedPosts.objects.filter(post_id=int(post_id), user_id=current_uid, following=0)
            if new_follow.count() > 0:
                new_follow = new_follow[0]
                new_follow.following = 1
                new_follow.save()
            else:
                new_follow = FollowedPosts(post_id=int(post_id), user_id=current_uid, date=dt.datetime.now(), following=1)
                new_follow.save()
            response_data["msg"] = word_list.filter(var_name="question-notifs-turned-on")[0].translation
        elif(operation == "unfollow"):
            follow = FollowedPosts.objects.filter(post_id=int(post_id), user_id=current_uid, following=1)[0]
            follow.following = 0
            follow.save()
            response_data["msg"] = word_list.filter(var_name="question-notifs-turned-off")[0].translation
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def get_searched_users(request):
    search_key = request.POST["search"]
    container = request.POST["container"]
    selectedUsers = request.POST["selectedUsers"]
    selected = selectedUsers.split(", ")
    bc = "bcgrayish"
    print(selected)
    if len(selected) > 0:
        selected = [int(i) for i in selected if i != '']
    followings = UserRelation.objects.filter(follower_id=current_uid)
    followings_ids = list({x.following.ID: x for x in followings}.keys())
    selected = selected + followings_ids
    selected.append(current_uid)
    print(selected)
    results = User.objects.filter(Q(display_name__icontains=search_key)|Q(user_login__icontains=search_key)).exclude(ID__in=selected)[:15]
    user_list = []
    for result in results:
        result = setup_current_user(result.ID)
        user_list.append(result)    
    return render(request, 'includes/select_user_list.html', {'user_list':user_list, 'container':container, 'bc':bc})

@csrf_exempt
def getsearchedpeople(request):
    search_key = request.POST["search"]
    selectedUsers = request.POST["selectedUsers"]
    selected = selectedUsers.split(", ")
    if len(selected) > 0:
        selected = [int(i) for i in selected if i != '']
    selected.append(current_uid)
    results = User.objects.filter(Q(display_name__icontains=search_key)|Q(user_login__icontains=search_key)).exclude(ID__in=selected)[:15]
    user_list = []
    for result in results:
        result = setup_current_user(result.ID)
        user_list.append(result)
    return render(request, 'includes/userlist.html', {'user_list':user_list})

@csrf_exempt
def requestanswer(request):
    response_data = {}
    try:
        selectedUsers = request.POST["selectedUsers"]
        post_id = int(request.POST["post_id"])
        selected = selectedUsers.split(", ")
        post = Post.objects.get(ID=post_id)
        if len(selected) > 0:
            selected = [int(i) for i in selected if i != '']
        for ID in selected:
            new_request = PostRequest(sender_id=current_uid, receiver_id=ID, post_id=post_id, date=dt.datetime.now(), answered=0, post_type=post.post_type)
            new_request.save()
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        response_data["msg"] = fun.ucfirst(word_list.filter(var_name="request-sent")[0].translation)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def saveanswerdraft(request):
    response_data = {}
    try:
        post_id = int(request.POST["post_id"])
        post_content = request.POST["post_content"]
        answer = Post.objects.filter(ID=post_id)[0]
        answer.post_content = post_content
        answer.post_modified = dt.datetime.now()
        answer.save()
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        response_data["msg"] = word_list.filter(var_name="answer-draft-saved")[0].translation
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def publishdraftanswer(request):
    response_data = {}
    try:
        post_id = int(request.POST["post_id"])
        post_content = request.POST["post_content"]
        answer = Post.objects.filter(ID=post_id)[0]
        answer.post_content = post_content
        answer.post_modified = dt.datetime.now()
        answer.post_status = "publish"
        answer.save()
        request = PostRequest.objects.filter(receiver_id=current_uid, post=answer.post_parent)
        if request.count() > 0:
            request[0].answered = 1
            request[0].save()
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        response_data["msg"] = word_list.filter(var_name="answer-published")[0].translation
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def deleteanswerdraft(request):
    response_data = {}
    try:
        post_id = int(request.POST["post_id"])
        answer = Post.objects.filter(ID=post_id)[0]
        answer.delete()
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        response_data["msg"] = word_list.filter(var_name="answer-deleted")[0].translation
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def checkusernameexists(request):
    response_data = {}
    try:
        username = request.POST["username"]
        query = User.objects.filter(user_login=username)
        if query.count() > 0:
            lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
            word_list = Languages.objects.filter(Q(lang_code = lang))
            response_data["content"] = word_list.filter(var_name="username-already-exists")[0].translation
        else:
            response_data["content"] = "success"
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def get_chat_item(request):
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    chats_data = json.loads(request.POST['chats'])
    chats = []
    for _, chat in chats_data.items():
        receivers = chat["receivers"]
        selected = receivers.split(", ")
        if len(selected) > 0:
            selected = [int(i) for i in selected if i != '' and int(i) != current_uid]
        results = User.objects.filter(ID__in=selected)
        user_list = []
        usernames = ""
        for result in results:
            result = setup_current_user(result.ID)
            user_list.append(result)
            usernames += "u/" + result.user_login + ","
        usernames = usernames[:-1]
        chat["receivers"] = user_list
        chat["usernames"] = usernames
        chat["datetime"] = dt.datetime.strptime(chat["datetime"], '%d/%m/%Y %H:%M:%S')
        chat["date"] = fun.humanizedate(chat["datetime"], word_list)
        chat["seen"] = int(chat["seen"])
        chat["sender"] = int(chat["sender"])
        if chat["msg"].startswith("<img data-type=") :
            msg = word_list.filter(var_name="user-sent-sosmoji")[0].translation
            sender = User.objects.get(ID=int(chat["sender"]))
            chat["msg"] = msg.replace("{user}", "u/"+sender.user_login)
        elif chat["msg"].startswith("<img src=") :
            msg = word_list.filter(var_name="user-sent-media")[0].translation
            sender = User.objects.get(ID=int(chat["sender"]))
            chat["msg"] = msg.replace("{user}", "u/"+sender.user_login)
        chats.append(chat)
    chats.sort(key=lambda x: x["datetime"], reverse=True)
    print(chats)
    return render(request, 'chat_item.html', {'chats':chats, 'current_uid':current_uid})

@csrf_exempt
def get_chat_popup_item(request):
    if current_uid:
        lang = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'language')[0].meta_value
    else:
        lang = "en-EN"
    word_list = Languages.objects.filter(Q(lang_code = lang))
    chats_data = json.loads(request.POST['chats'])
    chats = []
    for _, chat in chats_data.items():
        receivers = chat["receivers"]
        selected = receivers.split(", ")
        if len(selected) > 0:
            selected = [int(i) for i in selected if i != '' and int(i) != current_uid]
        results = User.objects.filter(ID__in=selected)
        user_list = []
        usernames = ""
        for result in results:
            result = setup_current_user(result.ID)
            user_list.append(result)
            usernames += "u/" + result.user_login + ","
        usernames = usernames[:-1]
        chat["receivers"] = user_list
        chat["usernames"] = usernames
        chat["datetime"] = dt.datetime.strptime(chat["datetime"], '%d/%m/%Y %H:%M:%S')
        chat["date"] = fun.humanizedate(chat["datetime"], word_list)
        chat["seen"] = int(chat["seen"])
        chat["sender"] = int(chat["sender"])
        if chat["msg"].startswith("<img data-type=") :
            msg = word_list.filter(var_name="user-sent-sosmoji")[0].translation
            sender = User.objects.get(ID=int(chat["sender"]))
            chat["msg"] = msg.replace("{user}", "u/"+sender.user_login)
        elif chat["msg"].startswith("<img src=") :
            msg = word_list.filter(var_name="user-sent-media")[0].translation
            sender = User.objects.get(ID=int(chat["sender"]))
            chat["msg"] = msg.replace("{user}", "u/"+sender.user_login)
        chats.append(chat)
    chats.sort(key=lambda x: x["datetime"], reverse=True)
    return render(request, 'chat_popup_item.html', {'chats':chats, 'current_uid':current_uid})

@csrf_exempt
def get_chat_right_menu(request):
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    receivers = request.POST['receivers']
    selected = receivers.split(", ")
    if len(selected) > 0:
        selected = [int(i) for i in selected if i != '' and int(i) != current_uid]
    results = User.objects.filter(ID__in=selected)
    user_list = []
    usernames = ""
    for result in results:
        result = setup_current_user(result.ID)
        user_list.append(result)
        usernames += "u/" + result.user_login + ","
    usernames = usernames[:-1]
    chat = {}
    if(len(user_list) == 1):
        current_user = setup_current_user(current_uid)
        current_followings = []
        for cf in current_user.followings:
            current_followings.append(cf.following.ID)
        common_followings = UserRelation.objects.filter(follower=user_list[0], following_id__in=current_followings)
        common_followings_list = []
        for cf in common_followings:
            try:
                cf = setup_current_user(cf.following_id)
                common_followings_list.append(cf)
            except:
                pass
        print(common_followings_list)
        chat["common_followings"] = common_followings_list
        followed_communities = FollowedCommunities.objects.filter(user_id = current_uid).order_by('-date').prefetch_related()
        community_ids = list({x.term_id: x for x in followed_communities}.keys())
        common_communities = FollowedCommunities.objects.filter(user_id = user_list[0].ID, term_id__in=community_ids).order_by('-date').prefetch_related()
        chat["common_communities"] = common_communities
    chat["receivers"] = user_list
    chat["usernames"] = usernames
    return render(request, 'chat_right_menu.html', {'chat':chat, 'current_uid':current_uid, 'word_list':word_list})

@csrf_exempt
def getsinglechatballoon(request):
    chat = {}
    chat["ID"] = request.POST["ID"]
    chat["sender"] = setup_current_user(int(request.POST["sender"]))
    chat["msg"] = request.POST["msg"]
    chat["date"] = request.POST["date"]
    media = False
    if chat["msg"].startswith("<img src=") :
        media = True
    return render(request, 'single_chat_balloon.html', {'chat':chat, 'current_uid':current_uid, 'media':media})

@csrf_exempt
def savesettings(request):
    response_data = {}
    try:
        settings_type = request.POST["type"]
        lang = UserMeta.objects.filter(user_id=current_uid, meta_key='language')[0].meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        if(settings_type == "feed"):
            nsfw = request.POST["nsfw"]
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='nsfw_preference')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='nsfw_preference', meta_value=nsfw)
                new_setting.save()
            else:
                my_setting.update(meta_value=nsfw)
            response_data["content"] = word_list.filter(var_name="changes_saved")[0].translation
        elif(settings_type == "chat"):
            chat_preference = request.POST["chat_preference"]
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='chat_preference')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='chat_preference', meta_value=chat_preference)
                new_setting.save()
            else:
                my_setting.update(meta_value=chat_preference)
            response_data["content"] = word_list.filter(var_name="changes_saved")[0].translation
        elif(settings_type == "notification"):
            comment_notif = request.POST["comment_notif"]
            answer_notif = request.POST["answer_notif"]
            post_notif_comm = request.POST["post_notif_comm"]
            post_notif_following = request.POST["post_notif_following"]
            following_notif = request.POST["following_notif"]
            birthday_notif = request.POST["birthday_notif"]
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='comment_notif_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='comment_notif_setting', meta_value=comment_notif)
                new_setting.save()
            else:
                my_setting.update(meta_value=comment_notif)
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='answer_notif_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='answer_notif_setting', meta_value=answer_notif)
                new_setting.save()
            else:
                my_setting.update(meta_value=answer_notif)
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='post_notif_comm_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='post_notif_comm_setting', meta_value=post_notif_comm)
                new_setting.save()
            else:
                my_setting.update(meta_value=post_notif_comm)
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='post_notif_following_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='post_notif_following_setting', meta_value=post_notif_following)
                new_setting.save()
            else:
                my_setting.update(meta_value=post_notif_following)
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='following_notif_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='following_notif_setting', meta_value=following_notif)
                new_setting.save()
            else:
                my_setting.update(meta_value=following_notif)
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='birthday_notif_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='birthday_notif_setting', meta_value=birthday_notif)
                new_setting.save()
            else:
                my_setting.update(meta_value=birthday_notif)
            response_data["content"] = word_list.filter(var_name="changes_saved")[0].translation
        elif(settings_type == "phone-privacy"):
            phone_privacy_setting = request.POST["phone-privacy"]
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='phone_privacy_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='phone_privacy_setting', meta_value=phone_privacy_setting)
                new_setting.save()
            else:
                my_setting.update(meta_value=phone_privacy_setting)
            response_data["content"] = word_list.filter(var_name="changes_saved")[0].translation
        elif(settings_type == "email-privacy"):
            email_privacy_setting = request.POST["email-privacy"]
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='email_privacy_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='email_privacy_setting', meta_value=email_privacy_setting)
                new_setting.save()
            else:
                my_setting.update(meta_value=email_privacy_setting)
            response_data["content"] = word_list.filter(var_name="changes_saved")[0].translation
        elif(settings_type == "location-privacy"):
            location_privacy_setting = request.POST["location-privacy"]
            my_setting = UserMeta.objects.filter(user_id=current_uid, meta_key='location_privacy_setting')
            if(my_setting.count() == 0):
                new_setting = UserMeta(user_id=current_uid, meta_key='location_privacy_setting', meta_value=location_privacy_setting)
                new_setting.save()
            else:
                my_setting.update(meta_value=location_privacy_setting)
            response_data["content"] = word_list.filter(var_name="changes_saved")[0].translation
    except:
        lang = "en-EN"
        try:
            lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        except:
            pass
        response_data["msg"] = Languages.objects.filter(lang_code=lang, var_name = 'general-error-msg')[0].translation 
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def searchusertoblock(request):
    search_key = request.POST["search"]
    current_user = setup_current_user(current_uid)
    selected = list({x.blocking_id: x for x in current_user.blocked}.keys())
    selected.append(current_uid)
    print(selected)
    results = User.objects.filter(Q(display_name__icontains=search_key)|Q(user_login__icontains=search_key)).exclude(ID__in=selected)[:5]
    response_data = {}
    for result in results:
        result = setup_current_user(result.ID)
        response_data[result.user_nicename] = "user!:!" + result.avatar_url + "!:!" + result.user_login
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def blockunblockuser(request):
    operation = request.POST["op"]
    user = request.POST["user"]
    print(user)
    uid = User.objects.filter(user_login=user)[0]
    if operation == "block":
        new_data = BlockedUsers(blocker_id=current_uid, blocking_id=uid.ID, date=dt.datetime.now())
        new_data.save()
    elif operation == "unblock":
        instance = BlockedUsers.objects.get(blocker_id=current_uid, blocking_id=uid.ID)
        instance.delete()
    return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def getreceivernames(request):
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    receivers = request.POST["receivers"]
    selected = receivers.split(", ")
    if len(selected) > 0:
        selected = [int(i) for i in selected if i != '' and int(i) != current_uid]
    usernames = []
    for s in selected:
        usernames.append(setup_current_user(s))
    return render(request, 'chat_receivers.html', {'users':usernames, 'current_user':current_user, 'word_list':word_list})

@csrf_exempt
def getchatpopupbox(request):
    print(current_uid)
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    chat = json.loads(request.POST['chat'])
    receivers = chat["users"]
    selected = receivers.split(", ")
    if len(selected) > 0:
        selected = [int(i) for i in selected if i != '' and int(i) != current_uid]
    results = User.objects.filter(ID__in=selected)
    user_list = []
    receiver_names = ""
    index = 1
    for result in results:
        result = setup_current_user(result.ID)
        user_list.append(result)
        if index == len(results):
            receiver_names += "u/" + result.user_login + ","
        else:
            receiver_names += "u/" + result.user_login
        index += 1
    if(len(user_list) == 1):
        chat["receiver"] = user_list[0]
    else:
        chat["receiver"] = user_list
        chat["receiver_names"] = receiver_names
        for msg in chat["messages"]:
            msg["sender"] = setup_current_user(int(msg["sender"]))
    return render(request, 'chat_popup_box.html', {'chat':chat, 'current_user':current_user, 'word_list':word_list})

@csrf_exempt
def getpostbyid(request):
    post_id = int(request.POST["postId"])
    post = Post.objects.filter(ID=post_id)[0]

    #lang = cache.get("current_user_lang")
    lang = None
    if not lang:
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    #cache.set("current_user_lang", lang, 86400)
    #cache_key = 'current_user_word_list'
    #word_list = cache.get(cache_key)
    word_list = None
    if not word_list:
        word_list = Languages.objects.filter(Q(lang_code = lang))
    #cache.set(cache_key, word_list, 86400)
    setup_postmeta(post, word_list)
    if post.post_type == "link":
        post.photo_from_url = fun.get_photo_from_url(post.post_content)
    elif post.post_type == "media":
        setup_mediameta(post)
    elif post.post_type == "quiz":
        post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
        post.post_title = post.post_title.replace(" - Sosyorol", "")
        if post.quiz_type == "media":
            setup_media_quizmeta(post, word_list)
        elif post.quiz_type == "colorBox":
            setup_colorbox_quizmeta(post, word_list)
        else:
            setup_quizmeta(post, word_list)
    post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
    post.comments = post.comments[:5]
    for comment in post.comments:
        comment.user = setup_current_user(comment.user.ID)
        comment.child_comments = Comment.objects.none()
        comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
        getgrandchildcomments(post.ID, comment.child_comments)
    return render(request, 'posts/get_single_post.html', {'post':post, 'word_list':word_list})

@csrf_exempt
def repost(request):
    repost_id = int(request.POST["postId"])
    repost_text = request.POST["txt"]
    parent = Post.objects.filter(ID=repost_id)[0]
    #cache_key = 'current_user'
    #cache_time = 86400
    #current_user = cache.get(cache_key)
    current_user = None
    if not current_user:
        current_user = setup_current_user(current_uid)
        #cache.set(cache_key, current_user, cache_time)
    #cache_key = 'current_user_lang'
    #lang = cache.get(cache_key)
    lang = None
    if not lang:
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        #cache.set(cache_key, lang, cache_time)
    #cache_key = 'current_user_word_list'
    #word_list = cache.get(cache_key)
    word_list = None
    if not word_list:
        word_list = Languages.objects.filter(Q(lang_code = lang))
        #cache.set(cache_key, word_list, cache_time)
    repost = Post(post_title=parent.post_title, post_content=repost_text, post_date=dt.datetime.now(), author=current_user,post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="repost", post_type="repost", post_excerpt=parent.post_excerpt, post_parent=repost_id)
    repost.save()
    response = dict()
    response["success"] = word_list.filter(var_name="repost_succesful")[0].translation
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def followunfollowcommunity(request):
    community_id = int(request.POST["community_id"])
    op = request.POST["op"]
    if op == "follow":
        query = FollowedCommunities.objects.filter(user_id=current_uid, term_id=community_id)
        if query.count() > 0:
            query = query[0]
            query.is_active = 1
        else:
            query = FollowedCommunities(user_id=current_uid, term_id=community_id, date=dt.datetime.now(), role="Member", is_active=1)
        query.save()
    elif op == "unfollow":
        query = FollowedCommunities.objects.filter(user_id=current_uid, term_id=community_id)[0]
        query.is_active = 0
        query.save() 
    return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def deletedraft(request):
    postId = int(request.POST["postId"])
    post = Post.objects.filter(ID=postId)[0]
    post.post_status = "deleted_draft"
    post.save()
    return HttpResponse(json.dumps({}), content_type="application/json")
'''---------------------------------------
  VIEWS              
-----------------------------------------'''
def opensosyorol(request):

    uid = None
    if 'uid' in request.COOKIES:
        uid = request.COOKIES["uid"].replace("%40", "@")
        print(uid)
        user = User.objects.get(user_email=uid)
        response = HttpResponseRedirect("/")
        response.set_cookie("uid", str(user.ID))
        return response
    else:
        try:
            uid = request.POST.get("uid")
            if uid is not None:
                uid = uid.replace("%40", "@")
                print(uid)
                user = User.objects.get(user_email=uid)
                response = HttpResponseRedirect("/")
                response.set_cookie("uid", str(user.ID))
                global current_uid
                current_uid = int(request.COOKIES["uid"].replace("sosyoroluseruid", ""))
                return response
        except:
            pass
    lang = "en-EN"
    dark = "light"
    word_list = Languages.objects.filter(lang_code = lang)
    country_list = Languages.objects.filter(var_name = 'lang')
    page_dict = sign_dictionary(word_list)
    return render(request, 'signin.html', {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict})

def signin(request):
    return opensosyorol(request)

def signup(request):
    try:
        uid = request.COOKIES["uid"]
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
    '''
    try:
        redirect = request.POST.get("uid")
    except:
        redirect = "/"
    '''
    global current_uid
    current_uid = None
    response = HttpResponseRedirect("/signin")
    response.delete_cookie("uid")
    return response

def resetpassword(request):
    lang = "en-EN"
    dark = ""
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    page_dict = sign_dictionary(word_list)
    return render(request, "resetpassword.html", {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict }) 

def verifyresetpassword(request):
    if request.GET.get("mode")  == "resetPassword" and request.GET.get("apiKey") == "AIzaSyA9jeHII9FVkhOQfCM_NyoifnN8eIN6EFM" and request.GET.get("oobCode") != None:
        mode = request.GET.get("mode")
        oobCode = request.GET.get("oobCode")
        lang = "en-EN"
        dark = ""
        word_list = Languages.objects.filter(Q(lang_code = lang))
        country_list = Languages.objects.filter(Q(var_name = 'lang'))
        page_dict = sign_dictionary(word_list)
        return render(request, "verifyresetpassword.html", {'lang':lang, 'dark':dark, 'country_list':country_list, 'page_dict':page_dict, 'mode':mode, 'oobCode':oobCode }) 
    else:
        return HttpResponseRedirect("/")

def phonecodeverification(request):
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
    import random
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return signin(request)
    page = "home"
    #cache_key = 'current_user' # needs to be unique
    #cache_time = 86400 # time in seconds for cache to be valid
    current_user = setup_current_user(current_uid)
    #cache_key = 'current_user_lang'
    #lang = cache.get(cache_key)
    lang = None
    if not lang:
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        #cache.set(cache_key, lang, cache_time)
    #cache_key = 'current_user_dark'
    #dark = cache.get(cache_key)
    dark = None
    if not dark:
        dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    print(dark)
        #cache.set(cache_key, dark, cache_time)

    #cache_key = 'current_user_word_list'
    #word_list = cache.get(cache_key)
    word_list = None
    if not word_list:
        word_list = Languages.objects.filter(Q(lang_code = lang))
        #cache.set(cache_key, word_list, cache_time)

    #cache_key = 'country_list'
    #country_list = cache.get(cache_key)
    country_list = None
    if not country_list:
        country_list = Languages.objects.filter(Q(var_name = 'lang'))
        #cache.set(cache_key, country_list, cache_time)

    #cache_key = 'followed_communities'
    #followed_communities = cache.get(cache_key)
    followed_communities = None
    if not followed_communities:
        followed_communities = FollowedCommunities.objects.filter(user_id = current_uid, is_active=1).order_by('-date').prefetch_related()
        #cache.set(cache_key, followed_communities, cache_time)

    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()

    #cache_key = 'home_posts_1_6' # needs to be unique
    #cache_time = 300 # time in seconds for cache to be valid
    #posts = cache.get(cache_key) # returns None if no key-value pair
    posts = None
    if not posts:
        start = time.time()
        posts, _ = get_feed_posts(1, 5)
        end = time.time() - start
        print(f"Get feed posts in {end} s")
        for post in posts:
            setup_postmeta(post, word_list)
            if post.post_type == "link":
                post.photo_from_url = fun.get_photo_from_url(post.post_content)
            elif post.post_type == "media":
                setup_mediameta(post)
            elif post.post_type == "poll":
                setup_pollmeta(post, word_list)
            elif post.post_type == "quiz":
                post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
                post.post_title = post.post_title.replace(" - Sosyorol", "")
                if post.quiz_type == "media":
                    setup_media_quizmeta(post, word_list)
                elif post.quiz_type == "colorBox":
                    setup_colorbox_quizmeta(post, word_list)
                else:
                    setup_quizmeta(post, word_list)
            post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
            post.comments = post.comments[:5]
            for comment in post.comments:
                comment.user = setup_current_user(comment.user.ID)
                comment.child_comments = Comment.objects.none()
                comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
                getgrandchildcomments(post.ID, comment.child_comments)
        #cache.set(cache_key, posts, cache_time)

    question_random = random.randint(1, 5)
    questions = get_suggested_questions(current_uid)

    community_random = random.randint(1, 5)
    communities = get_suggested_communities(current_uid)

    user_random = random.randint(1, 5)
    user_queryset = get_suggested_users2(current_uid)
    users = []
    for user in user_queryset:
        try:
            user_desc = UserMeta.objects.filter(user_id = user.ID, meta_key = 'description')[0]
            user.description = user_desc.meta_value
        except:
            pass
        user.avatar_url = setup_avatar_url(user.ID)
        users.append(user)

        '''
        start = time.time()
        comment_editor = comment_editor_dict(word_list)
        end = time.time() - start
        print(f"Setup comment editor in {end} s")
        
        start = time.time()
        notifications, num_notifications = setup_notifications(current_uid, word_list)
        end = time.time() - start
        print(f"Setup notifications in {end} s")'''
    return render(request, 'index.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user, 'page':page,
                                            'country_list':country_list, 'word_list':word_list,
                                            'followed_communities':followed_communities, 'popular_communities':popular_communities,
                                            'posts':posts, 'questions':questions,'communities':communities, 'users':users,
                                            'question_random':question_random, 'user_random':user_random, 'community_random':community_random,
                                            })
    '''return render(request, 'index.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                                'country_list':country_list, 'select_language':select_language,
                                                'followed_communities':followed_communities, 'feed_dict':feed_dict,
                                                'popular_communities':popular_communities, 'posts':posts,
                                                'post_template_dict':post_template_dict, 'comment_editor':comment_editor,
                                                'links':links, 'answers':answers, 'questions':questions, 'quizzes':quizzes,
                                                'communities':communities, 'users':users, 'polls':polls,
                                                'word_list':word_list, 'colorBox_quizzes':colorBox_quizzes, 'media_quizzes':media_quizzes, 'mediaposts':mediaposts,
                                                'notifications':notifications, 'num_notifications':num_notifications, 'page':page
                                                })'''

def search(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'language')[0].meta_value
    dark = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'mode')[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    search_key = ""
    try:
        search_key = request.POST["search_key"]
    except:
        try:
            search_key = request.GET.get("search_key")
        except:
            pass

    #Save search history
    search_history = SearchHistory.objects.filter(user_id=current_uid, search_term=search_key, is_deleted=0)
    if len(search_history) > 0:
        counter = search_history[0].counter + 1
        search_history.update(date=dt.datetime.now(), counter=counter)
    else:
        search_history = SearchHistory(user_id=current_uid, search_term=search_key, date=dt.datetime.now(), is_deleted=0, counter=1)
        search_history.save()

    #Left
    left_menu_dict = left_menu(word_list)
    post_types_dict = post_types(word_list)
    page_dict = search_page_dict(word_list)

    #Middle
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    fltr = "all"
    try:
        fltr = request.GET.get("filter")
        if fltr is None:
            fltr = "all"
    except:
        pass

    community_results = {}
    if fltr == "community" or fltr == "all":
        community_results = Community.objects.filter(Q(name__icontains=search_key))
        for community in community_results:
            follower_ids = FollowedCommunities.objects.filter(Q(term=community))
            follower_ids = list({x.user_id: x for x in follower_ids}.keys())
            community.followers = User.objects.filter(Q(ID__in=follower_ids))
    
    post_results = {}
    question_results = {}
    if fltr != "profile" and fltr != "community":
        post_results = Post.objects.filter(post_status="publish").filter(post_title__icontains=search_key).order_by('-post_date')
        if fltr == "post":
            post_results = post_results.filter(Q(post_type="post"))
        elif fltr == "link":
            post_results = post_results.filter(Q(post_type="link"))
        elif fltr == "poll":
            post_results = post_results.filter(Q(post_type="poll"))
        elif fltr == "quiz":
            post_results = post_results.filter(Q(post_type="quiz"))
        elif fltr == "question" or fltr == "all":
            question_results = post_results.filter(Q(post_type="questions"))
        elif fltr == "answer":
            post_results = post_results.filter(Q(post_type="answer"))
        elif fltr == "media":
            post_results = post_results.filter(Q(post_type="media"))
        for post in post_results:
            setup_postmeta(post, word_list)
            if post.post_type == "link":
                post.photo_from_url = fun.get_photo_from_url(post.post_content)
            if post.post_type == "media":
                setup_mediameta(post)
        for question in question_results:
            setup_postmeta(question, word_list)
    
    user_results = {}
    if fltr == "profile" or fltr == "all":
        user_results = User.objects.filter(Q(display_name__icontains=search_key))
        for user in user_results:
            user_desc = UserMeta.objects.filter(Q(user_id = user.ID)).filter(Q(meta_key = 'description'))[0]
            user.set_description(user_desc.meta_value)
            avatar_url = UserMeta.objects.filter(user=user, meta_key="avatar_url")[0].meta_value
            user.set_avatar(avatar_url)

    #Right
    right_menu_dict = right_menu(word_list)
    users = User.objects.all()[:2]
    for user in users:
        user_desc = UserMeta.objects.filter(Q(user_id = user.ID)).filter(Q(meta_key = 'description'))[0]
        user.set_description(user_desc.meta_value)
        avatar_url = UserMeta.objects.filter(user=user, meta_key="avatar_url")[0].meta_value
        user.set_avatar(avatar_url)
    return render(request, "search.html", {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list,
                                            'select_language':select_language, 'left_menu_dict':left_menu_dict,
                                            'right_menu_dict':right_menu_dict, 'users':users, 'post_types_dict':post_types_dict,
                                            'page_dict':page_dict, 'searchkey': search_key, 'community_results':community_results,
                                            'post_results':post_results, 'user_results':user_results, 'filter':fltr,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'question_results':question_results, 'word_list':word_list
                                            })

def history(request, **kwargs):
    import locale
    import re
    current_uid = get_current_uid(request)
    if current_uid == -1 :
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if 'filter' in kwargs:
        fltr = kwargs.get("filter").split("_")[0]
    else:
        fltr = "all"
    
    query = request.GET.get("query")
    if query is None:
        query = ""

    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    current_user = setup_current_user(current_uid)
    page_dict = history_dict(word_list)

    left_menu_dict = left_menu(word_list)
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = fun.ucfirst(c.translation)

    post_types_dict = post_types(word_list)
    search_history = SearchHistory.objects.filter(user_id=current_uid).filter(is_deleted=0).filter(search_term__icontains=query)
    post_history = PostHistory.objects.filter(user_id=current_uid).filter(is_deleted=0)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    for p in post_history:
        if fltr == "all" or fltr == p.post.post_type:
            setup_postmeta(p.post, word_list)
            if p.post.post_type == "media":
                setup_mediameta(p.post)
            elif p.post.post_type == "poll":
                setup_pollmeta(p.post, word_list)
            elif p.post.post_type == "link":
                p.post.photo_from_url = fun.get_photo_from_url(p.post.post_content)
            elif p.post.post_type == "questions":
                p.post.isanswered = isquestionanswered(p.post, current_uid)
                p.post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=p.post.ID)
                for answer in p.post.answers:
                    setup_postmeta(answer, word_list)
            elif p.post.post_type == "quiz":
                p.post.quiz_type = PostMeta.objects.filter(post_id=p.post.ID, meta_key="quiz_type")[0].meta_value
                p.post.post_title = p.post.post_title.replace(" - Sosyorol", "")
                setup_postmeta(p.post, word_list)
                if p.post.quiz_type == "media":
                    setup_media_quizmeta(p.post, word_list)
                elif p.post.quiz_type == "colorBox":
                    setup_colorbox_quizmeta(p.post, word_list)
                else:
                    setup_quizmeta(p.post, word_list)
            p.post.comments = Comment.objects.filter(comment_post=p.post, comment_parent=0).order_by('-comment_date').prefetch_related()
            p.post.comments = p.post.comments[:5]
            for comment in p.post.comments:
                comment.user = setup_current_user(comment.user.ID)
                comment.child_comments = Comment.objects.none()
                comment.child_comments = getchildcomments(p.post.ID, comment.comment_ID)
                getgrandchildcomments(p.post.ID, comment.child_comments)

    community_history = CommunityHistory.objects.filter(user_id=current_uid).filter(is_deleted=0)
    for c in community_history:
        follower_ids = FollowedCommunities.objects.filter(term=c.term)
        follower_ids = list({x.user_id: x for x in follower_ids}.keys())
        c.term.followers = User.objects.filter(ID__in=follower_ids)
            
    user_history = UserHistory.objects.filter(user_id=current_uid).filter(is_deleted=0)
    for user in user_history:
        user_desc = UserMeta.objects.filter(user_id = user.visited_user.ID).filter(meta_key = 'description')[0]
        user.visited_user.set_description(user_desc.meta_value)
        avatar_url = UserMeta.objects.filter(user=user.visited_user, meta_key="avatar_url")[0].meta_value
        user.visited_user.set_avatar(avatar_url)
    
    history = sorted(chain(search_history, post_history, community_history, user_history), key=lambda instance: instance.date, reverse=True)
    history_groups = {}
    for h in history:
        dict_key = h.date
        #locale.setlocale(locale.LC_TIME, lang.replace("-","_"))
        dict_key = dt.datetime.strftime(dict_key.date(), '%d %B %Y')
        if dict_key in history_groups:
            if h.history_type == "post":
                if re.search(query, h.post.post_title, re.IGNORECASE):
                    history_groups[dict_key].append(h)
            elif h.history_type == "community":
                if re.search(query, h.term.name, re.IGNORECASE):
                    history_groups[dict_key].append(h)
            elif h.history_type == "profile":
                if re.search(query, h.visited_user.display_name, re.IGNORECASE) or re.search(query, h.visited_user.user_login, re.IGNORECASE):
                    history_groups[dict_key].append(h)
            else:
                history_groups[dict_key].append(h)
        else:
            if fltr == "all" or fltr == h.history_type:
                if h.history_type == "post":
                    if re.search(query, h.post.post_title, re.IGNORECASE):
                        history_groups[dict_key] = [h]
                elif h.history_type == "community":
                    if re.search(query, h.term.name, re.IGNORECASE):
                        history_groups[dict_key] = [h]
                elif h.history_type == "profile":
                    if re.search(query, h.visited_user.display_name, re.IGNORECASE) or re.search(query, h.visited_user.user_login, re.IGNORECASE):
                        history_groups[dict_key] = [h]
                else:
                    history_groups[dict_key] = [h]
    history_groups = {k: history_groups[k] for k in list(history_groups.keys())[:5]}
    right_menu_dict = right_menu(word_list)
    users = User.objects.all()[:2]
    for user in users:
        user_desc = UserMeta.objects.filter(Q(user_id = user.ID)).filter(Q(meta_key = 'description'))[0]
        user.set_description(user_desc.meta_value)
        avatar_url = UserMeta.objects.filter(user=user, meta_key="avatar_url")[0].meta_value
        user.set_avatar(avatar_url)
    return render(request, "history.html", {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'right_menu_dict':right_menu_dict, 'users':users, 'post_types_dict':post_types_dict,
                                            'page_dict':page_dict, 'filter':fltr, 'history':history_groups,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict, 'query':query,
                                            'word_list':word_list})

@csrf_exempt
def lists(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    limit = 3
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    current_user = setup_current_user(current_uid)
    word_list = Languages.objects.filter(Q(lang_code = lang))
    left_menu_dict = left_menu(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = fun.ucfirst(c.translation)
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    #cache_time = 86400
    #cache_key = 'followed_communities'
    #followed_communities = cache.get(cache_key)
    followed_communities = None
    if not followed_communities:
        followed_communities = FollowedCommunities.objects.filter(user_id = current_uid, is_active=1).order_by('-date').prefetch_related()
        #cache.set(cache_key, followed_communities, cache_time)
    lists_dict = lists_achive(word_list)
    list_ids = ListUser.objects.filter(Q(user_id=current_uid)).order_by('-date')
    list_ids = list({x.list_id: x for x in list_ids}.keys())
    followedlists = List.objects.filter(Q(ID__in=list_ids)).order_by('-created_at')
    listsyoumaylike = List.objects.order_by('-created_at')[:3]
    for lst in listsyoumaylike:
        lst.posts = ListPost.objects.filter(Q(list_id=lst.ID))
        lst.members = ListUser.objects.filter(Q(list_id=lst.ID) & Q(role='member'))
        lst.followers = ListUser.objects.filter(Q(list_id=lst.ID) & Q(role='follower'))
    return render(request, 'lists/lists.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities, 'lists_dict':lists_dict,
                                            'listsyoumaylike':listsyoumaylike, 'followedlists':followedlists, 'limit':limit,
                                            'word_list':word_list
                                            })

def newpost(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    try:
        post_type = request.GET['post']
    except:
        post_type = "post"
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
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
    return render(request, 'newpost.html', {'post_type':post_type,'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict, 'post_types_dict':post_types_dict,
                                            'create_post_rules_dict': create_post_rules_dict, 'tips':tips, 'create_post_dict':create_post_dict,
                                            'newpost_actions_dict':newpost_actions_dict, 'drafts':drafts, 'word_list':word_list})

def createlist(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
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
    create_post_rules_dict = create_post_rules(word_list)
    return render(request, 'lists/newlist.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict, 
                                            'tips':tips, 'create_list_dict':create_list_dict,'word_list':word_list,
                                            'create_post_rules_dict':create_post_rules_dict})

def listdetail(request, slug, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if slug == "undefined" or slug == "create":
        return createlist(request)
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"

    lst = List.objects.get(url=slug)

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
    post_ids = ListPost.objects.filter(Q(list_id=lst.ID))
    lst.members = ListUser.objects.filter(Q(list_id=lst.ID, role="member"))
    lst.followers = ListUser.objects.filter(Q(list_id=lst.ID, role="follower"))
    current_user = setup_current_user(current_uid)
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
        elif post.post_type == "media":
            setup_mediameta(post)
        elif post.post_type == "poll":
            setup_pollmeta(post, word_list)
        elif post.post_type == "quiz":
            post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
            post.post_title = post.post_title.replace(" - Sosyorol", "")
            if post.quiz_type == "media":
                setup_media_quizmeta(post, word_list)
            elif post.quiz_type == "colorBox":
                setup_colorbox_quizmeta(post, word_list)
            else:
                setup_quizmeta(post, word_list)
        post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
        post.comments = post.comments[:5]
        for comment in post.comments:
            comment.user = setup_current_user(comment.user.ID)
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
            getgrandchildcomments(post.ID, comment.child_comments)

    left_menu_dict = left_menu(word_list)
    right_menu_dict = right_menu(word_list)
    list_dict = lists_achive(word_list)
    post_types_dict = post_types(word_list)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    return HttpResponse(render(request, 'lists/list_detail.html', {'list':lst, 'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict,
                                            'list_dict':list_dict, 'post_types_dict':post_types_dict,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'filter':fltr,'word_list':word_list}))

def listdetailfilter(request, slug, post_type):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    lst = List.objects.get(url=slug)
    post_ids = ListPost.objects.filter(Q(list_id=lst.ID))
    lst.members = ListUser.objects.filter(Q(list_id=lst.ID, role="member"))
    lst.followers = ListUser.objects.filter(Q(list_id=lst.ID, role="follower"))
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    avatar_url = UserMeta.objects.filter(user=current_user, meta_key="avatar_url")[0].meta_value
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
    return HttpResponse(render(request, 'lists/list_detail.html', {'list':lst, 'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'list_dict':list_dict, 'post_types_dict':post_types_dict,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'filter':fltr, 'word_list':word_list}))

def aboutlist(request, slug):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    lst = List.objects.get(url=slug)
    post_ids = ListPost.objects.filter(Q(list_id=lst.ID))
    lst.members = ListUser.objects.filter(Q(list_id=lst.ID, role="member"))
    lst.followers = ListUser.objects.filter(Q(list_id=lst.ID, role="follower"))
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    lst.posts = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')
    lst.creator_uname = User.objects.filter(Q(ID = lst.creator))[0].user_login
    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    avatar_url = UserMeta.objects.filter(user=current_user, meta_key="avatar_url")[0].meta_value
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
    return render(request, 'lists/aboutlist.html', {'list':lst, 'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'list_dict':list_dict, 'post_types_dict':post_types_dict,
                                            'list_info_dict':list_info_dict})

def savedposts(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    left_menu_dict = left_menu(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = fun.ucfirst(c.translation)
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    current_user = setup_current_user(current_uid)

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
    savedpostsobjs = SavedPosts.objects.filter(user_id=current_uid).order_by('-saved_at').prefetch_related()
    savedposts = []
    for item in savedpostsobjs:
        if fltr == "all" or item.post.post_type == fltr:
            setup_postmeta(item.post, word_list)
            if item.post.post_type == "link":
                item.post.photo_from_url = fun.get_photo_from_url(item.post.post_content)
            elif item.post.post_type == "media":
                setup_mediameta(item.post)
            elif item.post.post_type == "poll":
                setup_pollmeta(item.post, word_list)
            elif item.post.post_type == "quiz":
                item.post.quiz_type = PostMeta.objects.filter(post_id=item.post.ID, meta_key="quiz_type")[0].meta_value
                item.post.post_title = item.post.post_title.replace(" - Sosyorol", "")
                if item.post.quiz_type == "media":
                    setup_media_quizmeta(item.post, word_list)
                elif item.post.quiz_type == "colorBox":
                    setup_colorbox_quizmeta(item.post, word_list)
                else:
                    setup_quizmeta(item.post, word_list)
            item.post.comments = Comment.objects.filter(comment_post=item.post, comment_parent=0).order_by('-comment_date').prefetch_related()
            item.post.comments = item.post.comments[:5]
            for comment in item.post.comments:
                comment.user = setup_current_user(comment.user.ID)
                comment.child_comments = Comment.objects.none()
                comment.child_comments = getchildcomments(item.post.ID, comment.comment_ID)
                getgrandchildcomments(item.post.ID, comment.child_comments)
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
        avatar_url = UserMeta.objects.filter(user=user, meta_key="avatar_url")[0].meta_value
        user.set_avatar(avatar_url)
    return render(request, "savedposts.html", {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities, 'savedposts_dict':savedposts_dict,
                                            'post_types_dict':post_types_dict, 'savedposts':savedposts, 'filter': fltr,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict,
                                            'right_menu_dict':right_menu_dict, 'users':users, 'word_list':word_list
                                            })

def savedpostsfilter(request, post_type):
    return savedposts(request, filter=post_type)

def communities(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    page = "communities"
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    try:
        fromcompage = request.GET["fromcompage"]
        if fromcompage == "yes":
            return communitiesfiltered(request, filter=fltr)
    except:
        pass
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(var_name = 'lang')
    select_language = fun.ucfirst(word_list.filter(var_name = 'select-language')[0].translation)
    categories = CommunityCategories.objects.all()
    random_cat1 = categories.order_by('?')[0]
    random_cat2 = categories.order_by('?')[1]
    if fltr == "all":
        communities = Community.objects.all()[0:20]
    else:
        selected_category = CommunityCategories.objects.get(slug=fun.localized_upper(fltr))
        communities = CommunityCategoryRelation.objects.filter(category=selected_category)[:20]

    #cache_key = 'country_list'
    #cache_time = 86400
    #country_list = cache.get(cache_key)
    country_list = None
    if not country_list:
        country_list = Languages.objects.filter(Q(var_name = 'lang'))
        #cache.set(cache_key, country_list, cache_time)

    random_communities1 = CommunityCategoryRelation.objects.filter(category=random_cat1)[:5]
    random_communities2 = CommunityCategoryRelation.objects.filter(category=random_cat2)[:5]
    return render(request, 'communities/communities.html', {'current_user':current_user, 'lang':lang, 'darkmode':dark, 'dark':dark,
                                                            'word_list':word_list, 'country_list':country_list,
                                                            'country_list':country_list, 'select_language':select_language,
                                                            'categories':categories, 'communities':communities, 
                                                            'random_cat1':random_cat1, 'random_cat2':random_cat2,
                                                            'random_communities1':random_communities1, 'random_communities2':random_communities2, 
                                                            'filter':fltr, 'page':page })

def communitydetail(request, slug,  **kwargs):
    current_uid = get_current_uid(request)
    if slug == "lists":
        path = kwargs.get("filter")
        tokens = path.split("/")
        if (len(tokens) == 1):
            return listdetail(request, path)
        else:
            return listdetailfilter(request, tokens[0], post_type=tokens[1])
    elif slug == "communities/create":
        return newcommunity(request)

    community = Community.objects.filter(slug=slug)[0]
    taxonomy = TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
    post_ids = TermRelationship.objects.filter(term_taxonomy_id=taxonomy)
    post_ids = list({x.object_id: x for x in post_ids}.keys())
    community.posts = Post.objects.filter(ID__in=post_ids).order_by('-post_date')
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    if fltr == "post":
        community.posts = community.posts.filter(post_type="post")
    elif fltr == "link":
        community.posts = community.posts.filter(post_type="link")
    elif fltr == "poll":
        community.posts = community.posts.filter(post_type="poll")
    elif fltr == "quiz":
        community.posts = community.posts.filter(post_type="quiz")
    elif fltr == "answer":
        community.posts = community.posts.filter(post_type="answer")
    elif fltr == "question":
        community.posts = community.posts.filter(post_type="questions")
    elif fltr == "media":
        community.posts = community.posts.filter(post_type="media")

    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')
    index = 1
    for pc in popular_communities:
        if pc.term_id == community.term_id:
            community.rank = index
            break
        index += 1
    if community.rank == 0:
        community.rank = popular_communities.count() + 1

    community.posts = community.posts[:20]

    community.flairs = Flairs.objects.filter(term_id=community.term_id).filter(flair_type="post")
    if current_uid != -1:
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'language')[0].meta_value
        dark = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'mode')[0].meta_value
    else:
        current_user = None
        lang = "en-EN"
        dark = "light"
    word_list = Languages.objects.filter(lang_code = lang)

    #cache_key = 'country_list'
    #cache_time = 86400
    #country_list = cache.get(cache_key)
    country_list = None
    if not country_list:
        country_list = Languages.objects.filter(Q(var_name = 'lang'))
        #cache.set(cache_key, country_list, cache_time)
    if current_uid != -1:
        #Save history
        history = CommunityHistory.objects.filter(user_id=current_uid).filter(term=community).filter(is_deleted=0)
        if len(history) > 0:
            counter = history[0].counter + 1
            history.update(date=dt.datetime.now(), counter=counter)
        else:
            history = CommunityHistory(user_id=current_uid, term=community, date=dt.datetime.now(), is_deleted=0, counter=1)
            history.save()
        community.views += 1
        community.save()

    community.posts = community.posts[1:6]
    for post in community.posts:
        setup_postmeta(post, word_list)
        if post.post_type == "media":
            setup_mediameta(post)
        elif post.post_type == "poll":
            setup_pollmeta(post, word_list)
        elif post.post_type == "link":
            post.photo_from_url = fun.get_photo_from_url(post.post_content)
        elif post.post_type == "questions":
            post.isanswered = isquestionanswered(post, current_uid)
            post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=post.ID)
            for answer in post.answers:
                setup_postmeta(answer, word_list)
        elif post.post_type == "quiz":
            post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
            post.post_title = post.post_title.replace(" - Sosyorol", "")
            setup_postmeta(post, word_list)
            if post.quiz_type == "media":
                setup_media_quizmeta(post, word_list)
            elif post.quiz_type == "colorBox":
                setup_colorbox_quizmeta(post, word_list)
            else:
                setup_quizmeta(post, word_list)
        post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
        comment_length = len(post.comments)
        post.comments = post.comments[:5]
        for comment in post.comments:
            comment.user = setup_current_user(comment.user.ID)
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
            getgrandchildcomments(post.ID, comment.child_comments)
    post_types_dict = post_types(word_list)
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    feed_dict = feed(word_list)
    followers = FollowedCommunities.objects.filter(term_id=community.term_id)
    followings = []
    for f in followers:
        user = UserRelation.objects.filter(following_id=f.user_id).filter(follower_id=current_uid)
        if (len(user) > 0):
            user[0].following = setup_current_user(user[0].following.ID)
            followings.append(user[0])
    page_dict = communitydetail_dict(word_list, community.rank, followings)
    moderators = followers.filter(role="moderator")
    for m in moderators:
        m.user = setup_current_user(m.user_id)

    if FollowedCommunities.objects.filter(user=current_user, term=community, is_active=1).count() > 0:
        community.is_followed = True
    similars = []
    if current_uid != -1:
        similars = fun.find_similar_communities(community, current_user)[:3]
        for s in similars:
            if FollowedCommunities.objects.filter(user=current_user, term=community, is_active=1).count() > 0:
                s.is_followed = True
    else:
        taxonomies = TermTaxonomy.objects.filter(term_id=community.term_id)
        post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomies)
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        posts = Post.objects.filter(ID__in=post_ids)
        similars = []
        for post in posts:
            community_taxonomy_ids = TermRelationship.objects.filter(object_id=post.ID)
            community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
            community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
            community_ids = list({x.term_id: x for x in community_ids if x.term_id != community.term_id}.keys())
            comms = Community.objects.filter(term_id__in=community_ids)
            for c in comms:
                if not c in similars:
                    similars.append(c)
        similars = similars[:6]


    #cache_key = 'followed_communities'
    #followed_communities = cache.get(cache_key)
    followed_communities = None
    if current_uid != -1:
        if not followed_communities:
            followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
            #cache.set(cache_key, followed_communities, cache_time)
    try:
        category_item = CommunityCategoryRelation.objects.filter(community=community)[0]
        category = CommunityCategories.objects.get(term_id=category_item.category_id).slug
    except:
        category = None

    return render(request, 'communities/communitydetail.html', {'community':community, 'country_list':country_list, 'lang':lang, 'darkmode':dark, 'dark':dark,
                                                                'post_types_dict':post_types_dict, 'filter':fltr,
                                                                'feed_dict':feed_dict, 'page_dict':page_dict, 'followed_communities':followed_communities,
                                                                'followers':followers, 'comment_editor':comment_editor,
                                                                'post_template_dict': post_template_dict, 'followings':followings,
                                                                'moderators':moderators, 'current_user': current_user, 'word_list':word_list,
                                                                'similars':similars, 'category':category
                                                                })

def communityfollowers(request, slug,  **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    community = Community.objects.filter(slug=slug)[0]
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')
    index = 1
    for pc in popular_communities:
        if pc.term_id == community.term_id:
            community.rank = index
            break
        index += 1
    if community.rank == 0:
        community.rank = popular_communities.count() + 1

    community.posts = community.posts[:20]
    community.flairs = Flairs.objects.filter(term_id=community.term_id).filter(flair_type="post")

    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'language')[0].meta_value
    dark = UserMeta.objects.filter(user_id = current_uid).filter(meta_key = 'mode')[0].meta_value
    word_list = Languages.objects.filter(lang_code = lang)

    #cache_key = 'country_list'
    #cache_time = 86400
    #country_list = cache.get(cache_key)
    country_list = None
    if not country_list:
        country_list = Languages.objects.filter(Q(var_name = 'lang'))
        #cache.set(cache_key, country_list, cache_time)
    
    post_types_dict = post_types(word_list)

    feed_dict = feed(word_list)
    followers = FollowedCommunities.objects.filter(term_id=community.term_id)
    community_followers = []
    for f in followers:
        try:
            user = User.objects.filter(ID=f.user_id)
            user = setup_current_user(f.user_id)
            community_followers.append(user)
        except:
            print("pass")
            pass
            
    page_dict = communitydetail_dict(word_list, community.rank, community_followers)
    moderators = followers.filter(role="moderator")
    for m in moderators:
        m.user = setup_current_user(m.user_id)

    is_followed = False 
    if FollowedCommunities.objects.filter(user=current_user, term=community, is_active=1).count() > 0:
        is_followed = True

    #cache_key = 'followed_communities'
    #followed_communities = cache.get(cache_key)
    followed_communities = None
    if not followed_communities:
        followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
        #cache.set(cache_key, followed_communities, cache_time)
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    return render(request, 'communities/communityfollowers.html', {'community':community, 'country_list':country_list,
                                                                'post_types_dict':post_types_dict, 'feed_dict':feed_dict, 'darkmode':dark, 'dark':dark,
                                                                'page_dict':page_dict, 'followed_communities':followed_communities,
                                                                'followers':followers, 'followtxt':followtxt, 'followingtxt':followingtxt,
                                                                'community_followers':community_followers, 'moderators':moderators, 'current_user': current_user, 
                                                                'word_list':word_list, 'is_followed':is_followed
                                                                })

def newcommunity(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    left_menu_dict = left_menu(word_list)
    tips = fun.ucwords(word_list.filter(Q(var_name = 'tips'))[0].translation)
    communitycats = CommunityCategories.objects.all().order_by("name")
    create_list_dict = create_community(word_list)
    new_community_tips_dict = new_community_tips(word_list)
    return render(request, 'communities/newcommunity.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'left_menu_dict':left_menu_dict, 
                                            'tips':tips, 'create_list_dict':create_list_dict, 'communitycats':communitycats,
                                            'new_community_tips_dict':new_community_tips_dict, 'word_list':word_list})

def postdetail(request, username, post_id, slug):
    current_uid = get_current_uid(request)
    ref = ""
    try:
        ref = request.GET["ref"]
    except:
        pass
    if len(slug.split("/")) > 1:
        return editpost(request, username, post_id, slug)
    pid = int(post_id.replace("s", "x"), 16) - 100000
    post = Post.objects.filter(ID=pid)[0]

    if current_uid != -1:
        #Save history
        history = PostHistory.objects.filter(user_id=current_uid, post=post, is_deleted=0)
        if len(history) > 0:
            counter = history[0].counter + 1
            history.update(date=dt.datetime.now(), counter=counter)
        else:
            history = PostHistory(user_id=current_uid, post=post, date=dt.datetime.now(), is_deleted=0, counter=1)
            history.save()

    community_taxonomy_ids = TermRelationship.objects.filter(object_id=post.ID)
    community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
    community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
    community_ids = list({x.term_id: x for x in community_ids}.keys())
    post.communities = Community.objects.filter(term_id__in=community_ids)
    for community in post.communities:
        community.views += 1
        community.save()
    if post.communities.count() > 0:
        post.first_community = post.communities[0].name
    if current_uid != -1:
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        dark = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'mode').meta_value
    else:
        current_user = None
        lang = "en-EN"
        dark = "light"
    word_list = Languages.objects.filter(lang_code = lang)
    setup_postmeta(post, word_list)
    post.author = setup_current_user(post.author.ID)
    if post.post_type == "media":
        setup_mediameta(post)
    elif post.post_type == "poll":
        setup_pollmeta(post, word_list)
    elif post.post_type == "link":
        post.photo_from_url = fun.get_photo_from_url(post.post_content)
    elif post.post_type == "questions":
        post.isanswered = isquestionanswered(post, current_uid)
        post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=post.ID)
        for answer in post.answers:
            setup_postmeta(answer, word_list)
    elif post.post_type == "quiz":
        post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
        post.post_title = post.post_title.replace(" - Sosyorol", "")
        setup_postmeta(post, word_list)
        if post.quiz_type == "media":
            setup_media_quizmeta(post, word_list)
        elif post.quiz_type == "colorBox":
            setup_colorbox_quizmeta(post, word_list)
        else:
            setup_quizmeta(post, word_list)
    followed_communities = FollowedCommunities.objects.filter(user_id = current_uid).order_by('-date').prefetch_related()
    post.flairs = PostFlair.objects.filter(post=post)
    post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
    comment_length = len(post.comments)
    post.comments = post.comments[:5]
    for comment in post.comments:
        comment.user = setup_current_user(comment.user.ID)
        comment.child_comments = Comment.objects.none()
        comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
        getgrandchildcomments(post.ID, comment.child_comments)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    more_from_content_owner = word_list.filter(var_name="more_from_content_owner")[0].translation
    more_from_content_owner = more_from_content_owner.replace("{user}", "<a class='fs19 title ctitle underline-on-hover' href='/u/"+post.author.user_login+"'>"+post.author.user_login+"</a>")
    other_posts = Post.objects.filter(post_author=post.post_author, post_status="publish", post_type__in=["post", "quiz", "poll", "answer", "questions", "link", "media"]).exclude(ID=post.ID).order_by('-post_date')[:3]
    for op in other_posts:
        setup_postmeta(op, word_list)
        community_taxonomy_ids = TermRelationship.objects.filter(object_id=op.ID)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        op.communities = Community.objects.filter(term_id__in=community_ids)[:3]
    return render(request, 'postdetail.html', {'post':post, 'lang':lang, 'darkmode':dark, 'dark':dark,
                                                'current_user': current_user, 'word_list':word_list,
                                                'followed_communities':followed_communities, 'comments':post.comments, 'comment_length':comment_length,
                                                'ref':ref, 'notifications':notifications, 'num_notifications':num_notifications,
                                                'followtxt': followtxt, 'followingtxt':followingtxt, 'more_from_content_owner':more_from_content_owner,
                                                'other_posts': other_posts
                                                })

def editpost(request, username, post_id, slug):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    pid = int(post_id.replace("s", "x"), 16) - 100000
    post = Post.objects.filter(ID=pid)[0]
    if post.post_author != current_uid:
        return HttpResponseRedirect("/u/"+username+"/"+post_id+"/"+slug)
    else:
        community_taxonomy_ids = TermRelationship.objects.filter(object_id=post.ID)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        post.communities = Community.objects.filter(term_id__in=community_ids)
        for community in post.communities:
            community.views += 1
            community.save()
        if post.communities.count() > 0:
            post.first_community = post.communities[0].name
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
        dark = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'mode').meta_value
        word_list = Languages.objects.filter(lang_code = lang)
        setup_postmeta(post, word_list)
        create_post_dict = {}
        if(post.post_type == "poll"):
            print(post.post_type)
            create_post_dict = create_poll(word_list)
            print(create_post_dict)
        post.author = setup_current_user(post.author.ID)
        if post.post_type == "media":
            setup_mediameta(post)
        elif post.post_type == "poll":
            setup_pollmeta(post, word_list)
        elif post.post_type == "link":
            post.photo_from_url = fun.get_photo_from_url(post.post_content)
        elif post.post_type == "questions":
            post.isanswered = isquestionanswered(post, current_uid)
            post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=post.ID)
            for answer in post.answers:
                setup_postmeta(answer, word_list)
        elif post.post_type == "quiz":
            post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
            post.post_title = post.post_title.replace(" - Sosyorol", "")
            setup_postmeta(post, word_list)
            if post.quiz_type == "media":
                setup_media_quizmeta(post, word_list)
            elif post.quiz_type == "colorBox":
                setup_colorbox_quizmeta(post, word_list)
            else:
                setup_quizmeta(post, word_list)
        followed_communities = FollowedCommunities.objects.filter(user_id = current_uid).order_by('-date').prefetch_related()
        post.flairs = PostFlair.objects.filter(post=post)
        post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
        comment_length = len(post.comments)
        post.comments = post.comments[:5]
        for comment in post.comments:
            comment.user = setup_current_user(comment.user.ID)
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
            getgrandchildcomments(post.ID, comment.child_comments)
        notifications, num_notifications = setup_notifications(current_uid, word_list)
        followtxt = word_list.filter(var_name="follow")[0].translation
        followingtxt = word_list.filter(var_name="following")[0].translation
        more_from_content_owner = word_list.filter(var_name="more_from_content_owner")[0].translation
        more_from_content_owner = more_from_content_owner.replace("{user}", "<a class='fs19 title ctitle underline-on-hover' href='/u/"+post.author.user_login+"'>"+post.author.user_login+"</a>")
        other_posts = Post.objects.filter(post_author=post.post_author, post_status="publish", post_type__in=["post", "quiz", "poll", "answer", "questions", "link", "media"]).exclude(ID=post.ID).order_by('-post_date')[:3]
        for op in other_posts:
            setup_postmeta(op, word_list)
            community_taxonomy_ids = TermRelationship.objects.filter(object_id=op.ID)
            community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
            community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
            community_ids = list({x.term_id: x for x in community_ids}.keys())
            op.communities = Community.objects.filter(term_id__in=community_ids)[:3]
        left_menu_dict = left_menu(word_list)
        post_types_dict = post_types(word_list)
        create_post_rules_dict = create_post_rules(word_list)
        tips = fun.ucwords(word_list.filter(var_name = 'tips')[0].translation)
        newpost_actions_dict = newpost_actions(word_list)
        drafts = Post.objects.filter(author_id=current_uid).filter(post_status="draft").filter(post_type__in=["post", "questions","poll"]).order_by('post_date')
        for draft in drafts:
            setup_postmeta(draft, word_list)
        return render(request, 'editpost.html', {'currentpost':post, 'lang':lang, 'darkmode':dark, 'dark':dark,
                                                'current_user': current_user, 'word_list':word_list,
                                                'followed_communities':followed_communities, 'comments':post.comments, 'comment_length':comment_length,
                                                'notifications':notifications, 'num_notifications':num_notifications,
                                                'followtxt': followtxt, 'followingtxt':followingtxt, 'more_from_content_owner':more_from_content_owner,
                                                'other_posts': other_posts, 'left_menu_dict': left_menu_dict, 'post_types_dict':post_types_dict,
                                                'create_post_rules_dict': create_post_rules_dict, 'tips':tips, 'create_post_dict':create_post_dict,
                                                'newpost_actions_dict':newpost_actions_dict, 'drafts':drafts
                                                })
      
def answerdetail(request, parent_author_name, parent_post_id, parent_slug, author_name):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    pid = int(parent_post_id.replace("s", "x"), 16) - 100000
    author = User.objects.filter(user_login=author_name)[0]
    post = Post.objects.filter(post_parent=pid, post_author=author.ID, post_type="answer", post_status="publish")[0]
    post.parent = Post.objects.filter(ID=pid)[0]
    post.parent.guid = arrange_post_slug(post.parent.post_title)
    post.parent.hex_id = hex(post.parent.ID + 100000).replace("x", "s")
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    setup_postmeta(post, word_list)
    post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
    comment_length = len(post.comments)
    post.comments = post.comments[:5]
    for comment in post.comments:
        comment.user = setup_current_user(comment.user.ID)
        comment.child_comments = Comment.objects.none()
        comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
        getgrandchildcomments(post.ID, comment.child_comments)
    more_from_content_owner = word_list.filter(var_name="more_from_content_owner")[0].translation
    more_from_content_owner = more_from_content_owner.replace("{user}", "<a class='fs19 title ctitle underline-on-hover' href='/u/"+post.author.user_login+"'>"+post.author.user_login+"</a>")
    other_posts = Post.objects.filter(post_author=post.post_author, post_status="publish", post_type__in=["post", "quiz", "poll", "answer", "questions", "link", "media"]).exclude(ID=post.ID).order_by('-post_date')[:3]
    for op in other_posts:
        setup_postmeta(op, word_list)
        community_taxonomy_ids = TermRelationship.objects.filter(object_id=op.ID)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        op.communities = Community.objects.filter(term_id__in=community_ids)[:3]
    return render(request, 'answerdetail.html', {'post':post, 'lang':lang, 'darkmode':dark, 'dark':dark, 
                                                'current_user': current_user, 'word_list':word_list,
                                                'followed_communities':followed_communities, 'comments':post.comments, 'comment_length':comment_length,
                                                'more_from_content_owner':more_from_content_owner, 'other_posts':other_posts,
                                                })

def editanswer(request, parent_author_name, parent_post_id, parent_slug, author_name):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    pid = int(parent_post_id.replace("s", "x"), 16) - 100000
    author = User.objects.filter(user_login=author_name)[0]
    post = Post.objects.filter(post_parent=pid, post_author=author.ID, post_type="answer", post_status="publish")[0]
    if post.post_author != current_uid:
        return HttpResponseRedirect("/u/"+parent_author_name+"/"+parent_post_id+"/"+parent_slug+"/"+author_name)
    post.parent = Post.objects.filter(ID=pid)[0]
    post.parent.guid = arrange_post_slug(post.parent.post_title)
    post.parent.hex_id = hex(post.parent.ID + 100000).replace("x", "s")
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    setup_postmeta(post, word_list)
    post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
    comment_length = len(post.comments)
    post.comments = post.comments[:5]
    for comment in post.comments:
        comment.user = setup_current_user(comment.user.ID)
        comment.child_comments = Comment.objects.none()
        comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
        getgrandchildcomments(post.ID, comment.child_comments)
    left_menu_dict = left_menu(word_list)
    post_types_dict = post_types(word_list)
    create_post_rules_dict = create_post_rules(word_list)
    tips = fun.ucwords(word_list.filter(var_name = 'tips')[0].translation)
    newpost_actions_dict = newpost_actions(word_list)
    drafts = Post.objects.filter(author_id=current_uid).filter(post_status="draft").filter(post_type__in=["post", "questions","poll"]).order_by('post_date')
    for draft in drafts:
        setup_postmeta(draft, word_list)
    setup_postmeta(post.parent, word_list)
    community_taxonomy_ids = TermRelationship.objects.filter(object_id=post.parent.ID)
    community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
    community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
    community_ids = list({x.term_id: x for x in community_ids}.keys())
    post.parent.communities = Community.objects.filter(term_id__in=community_ids)
    for community in post.parent.communities:
        community.save()
    if post.parent.communities.count() > 0:
        post.parent.first_community = post.parent.communities[0].name
    post.parent.flairs = PostFlair.objects.filter(post=post.parent)
    return render(request, 'editpost.html', {'post':post, 'lang':lang, 'darkmode':dark, 'dark':dark,
                                                'current_user': current_user, 'word_list':word_list, 'currentpost':post, 'question':post.parent,
                                                'followed_communities':followed_communities, 'comments':post.comments, 'comment_length':comment_length,
                                                'left_menu_dict':left_menu_dict, 'post_types_dict':post_types_dict, 'create_post_rules_dict':create_post_rules_dict,
                                                'tips':tips, 'newpost_actions_dict':newpost_actions_dict, 'drafts':drafts
                                                })

def userprofile(request, username,  **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    ref = ""
    try:
        ref = request.GET["ref"]
    except:
        pass
    current_user = setup_current_user(current_uid)
    profile = setup_current_user(User.objects.filter(user_login=username)[0].ID)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    post_length = profile.posts.count()
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    if fltr == "post":
        profile.posts = profile.posts.filter(post_type="post")
    elif fltr == "link":
        profile.posts = profile.posts.filter(post_type="link")
    elif fltr == "poll":
        profile.posts = profile.posts.filter(post_type="poll")
    elif fltr == "quiz":
        profile.posts = profile.posts.filter(post_type="quiz")
    elif fltr == "answers":
        fltr = "answer"
        profile.posts = profile.posts.filter(post_type="answer")
    elif fltr == "question":
        profile.posts = profile.posts.filter(post_type="questions")
    elif fltr == "media":
        profile.posts = profile.posts.filter(post_type="media")

    for f in profile.followers:
        f.follower.avatar_url = setup_avatar_url(f.follower.ID)
        
    if fltr == 'comments':
        profile.comments = Comment.objects.filter(user=profile).order_by("-comment_date")
        for comment in profile.comments:
            #comment.comment_post = Post.objects.filter(ID=comment.comment_post_ID)[0]
            #comment.comment_post = setup_postmeta(comment.comment_post, word_list)
            comment.comment_post.post_title = comment.comment_post.post_title.replace(" - Sosyorol", "")
            comment.user = profile
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(comment.comment_post.ID, comment.comment_ID)
            getgrandchildcomments(comment.comment_post.ID, comment.child_comments)
    else:
        index = 0
        print(profile.posts)
        for post in profile.posts:
            if index <= 5:
                setup_postmeta(post, word_list)
                if post.post_status == "publish":
                    if post.post_type == "media":
                        setup_mediameta(post)
                    elif post.post_type == "poll":
                        setup_pollmeta(post, word_list)
                    elif post.post_type == "link":
                        post.photo_from_url = fun.get_photo_from_url(post.post_content)
                    elif post.post_type == "questions":
                        setup_postmeta(post, word_list)
                        post.isanswered = isquestionanswered(post, current_uid)
                        post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=post.ID)
                        for answer in post.answers:
                            setup_postmeta(answer, word_list)
                    elif post.post_type == "quiz":
                        post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
                        post.post_title = post.post_title.replace(" - Sosyorol", "")
                        setup_postmeta(post, word_list)
                        if post.quiz_type == "media":
                            setup_media_quizmeta(post, word_list)
                        elif post.quiz_type == "colorBox":
                            setup_colorbox_quizmeta(post, word_list)
                        else:
                            setup_quizmeta(post, word_list)
                elif post.post_status == "repost":
                    post.parent = Post.objects.filter(ID=post.post_parent)[0]
                    setup_postmeta(post.parent, word_list)
                    if post.parent.post_type == "link":
                        post.parent.photo_from_url = fun.get_photo_from_url(post.parent.post_content)
                    elif post.post_type == "poll":
                        setup_pollmeta(post, word_list)
                    elif post.parent.post_type == "media":
                        setup_mediameta(post.parent)
                    elif post.parent.post_type == "quiz":
                        post.parent.quiz_type = PostMeta.objects.filter(post_id=post.parent.ID, meta_key="quiz_type")[0].meta_value
                        post.parent.post_title = post.parent.post_title.replace(" - Sosyorol", "")
                        if post.parent.quiz_type == "media":
                            setup_media_quizmeta(post.parent, word_list)
                        elif post.parent.quiz_type == "colorBox":
                            setup_colorbox_quizmeta(post.parent, word_list)
                        else:
                            setup_quizmeta(post.parent, word_list)
                    post.parent.comments = Comment.objects.filter(comment_post=post.parent, comment_parent=0).order_by('-comment_date').prefetch_related()
                    post.parent.comments = post.parent.comments[:5]
                    for comment in post.parent.comments:
                        comment.user = setup_current_user(comment.user.ID)
                        comment.child_comments = Comment.objects.none()
                        comment.child_comments = getchildcomments(post.parent.ID, comment.comment_ID)
                        getgrandchildcomments(post.parent.ID, comment.child_comments)
                post.comments = Comment.objects.filter(comment_post=post, comment_parent=0).order_by('-comment_date').prefetch_related()
                post.comments = post.comments[:5]
                for comment in post.comments:
                    comment.user = setup_current_user(comment.user.ID)
                    comment.child_comments = Comment.objects.none()
                    comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
                    getgrandchildcomments(post.ID, comment.child_comments)
            else:
                break
            index += 1
    profile.posts = profile.posts[:5]
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    employments = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'employments').order_by('-umeta_id')
    profile.employment_credentials = []
    if employments.count() > 0:
        current_employment = json.loads(employments[0].meta_value)
        position = current_employment["position"]
        company = current_employment["company"]
        profile.employments = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
        for employment in employments:
            credential = dict()
            credential["ID"] = employment.umeta_id
            current_employment = json.loads(employment.meta_value)
            position = current_employment["position"]
            credential["position"] = position
            credential["startDate"] = current_employment["startDate"]
            credential["endDate"] = current_employment["endDate"]
            company = current_employment["company"]
            credential["company"] = company
            cred = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
            credential["cred"] = cred
            profile.employment_credentials.append(credential)
        
    educations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'educations').order_by('-umeta_id')
    profile.education_credentials = []
    if educations.count() > 0:
        current_education = json.loads(educations[0].meta_value)
        school = current_education["school"]
        major = current_education["major"]
        degree = current_education["degree"]
        graduation = current_education["graduation"]
        profile.educations = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
        datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
        now = dt.datetime.now()
        if datetime_object > now:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
        else:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
        for education in educations:
            credential = dict()
            credential["ID"] = education.umeta_id
            current_education = json.loads(education.meta_value)
            school = current_education["school"]
            credential["school"] = school
            major = current_education["major"]
            credential["major"] = major
            credential["minor"] = current_education["minor"]
            degree = current_education["degree"]
            credential["degree"] = degree
            graduation = current_education["graduation"]
            credential["graduation"] = graduation
            cred = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
            datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
            else:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
            credential["cred"] = cred
            profile.education_credentials.append(credential)

    
    locations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'locations').order_by('-umeta_id')
    profile.location_credentials = []
    if locations.count() > 0:
        current_location = json.loads(locations[0].meta_value)
        location = current_location["location"]
        startDate = current_location["startDate"]
        endDate = current_location["endDate"]
        if endDate == "current":
            profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
        else:
            datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                profile.locations = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
        for location in locations:
            credential = dict()
            credential["ID"] = location.umeta_id
            current_location = json.loads(location.meta_value)
            location = current_location["location"]
            credential["location"] = location
            startDate = current_location["startDate"]
            credential["startDate"] = startDate
            endDate = current_location["endDate"]
            credential["endDate"] = endDate
            if endDate == "current":
                cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
                now = dt.datetime.now()
                if datetime_object > now:
                    cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
                else:
                    cred = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
            credential["cred"] = cred
            profile.location_credentials.append(credential)

    
    languages = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'languages').order_by('-umeta_id')
    profile.language_credentials = []
    if languages.count() > 0:
        current_language = json.loads(languages[0].meta_value)
        language = current_language["language"]
        language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
        language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
        profile.languages = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
        for l in languages:
            credential = dict()
            credential["ID"] = l.umeta_id
            current_language = json.loads(l.meta_value)
            language = current_language["language"]
            credential["language"] = language
            language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
            language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
            cred = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
            credential["cred"] = cred
            profile.language_credentials.append(credential)
    
    photos = PostMeta.objects.filter(meta_key="media_type", meta_value="image")
    photos = list({x.post_id: x for x in photos}.keys())
    medias = Post.objects.filter(ID__in=photos, post_author=profile.ID, post_status="publish", post_type="media").order_by('-post_date')[:6]
    for media in medias:
        setup_postmeta(media, word_list)
        setup_mediameta(media)
    empty_medias = 6 - medias.count()
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    suggesteds = get_suggested_users(word_list, current_user)
    if len(suggesteds) == 0:
        suggesteds.extend(get_suggested_users2(current_uid))
        for user in suggesteds:
            user.avatar_url = setup_avatar_url(user.ID)
    if profile.ID != current_uid:
        #Save history
        history = UserHistory.objects.filter(user_id=profile.ID, visited_user_id=current_uid, is_deleted=0)
        if len(history) > 0:
            counter = history[0].counter + 1
            history.update(date=dt.datetime.now(), counter=counter)
        else:
            history = UserHistory(user_id=profile.ID, visited_user_id=current_uid, date=dt.datetime.now(), is_deleted=0, counter=1)
            history.save()
    return render(request, 'profile.html', {'current_user':current_user, 'lang':lang, 'darkmode':dark, 'dark':dark, 'word_list':word_list, 
                                            'profile':profile, 'filter':fltr, 'country_list':country_list, 'medias':medias,
                                            'empty_medias':range(empty_medias), 'followtxt':followtxt, 'followingtxt':followingtxt,
                                            'ref':ref, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'users': suggesteds, 'post_length':post_length
                                            })

def userfollowers(request, username):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    profile = setup_current_user(User.objects.filter(user_login=username)[0].ID)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for f in profile.followers:
        f.follower.avatar_url = setup_avatar_url(f.follower.ID)
    employments = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'employments').order_by('-umeta_id')
    profile.employment_credentials = []
    if employments.count() > 0:
        current_employment = json.loads(employments[0].meta_value)
        position = current_employment["position"]
        company = current_employment["company"]
        profile.employments = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
        for employment in employments:
            credential = dict()
            credential["ID"] = employment.umeta_id
            current_employment = json.loads(employment.meta_value)
            position = current_employment["position"]
            credential["position"] = position
            credential["startDate"] = current_employment["startDate"]
            credential["endDate"] = current_employment["endDate"]
            company = current_employment["company"]
            credential["company"] = company
            cred = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
            credential["cred"] = cred
            profile.employment_credentials.append(credential)
    
    educations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'educations').order_by('-umeta_id')
    profile.education_credentials = []
    if educations.count() > 0:
        current_education = json.loads(educations[0].meta_value)
        school = current_education["school"]
        major = current_education["major"]
        degree = current_education["degree"]
        graduation = current_education["graduation"]
        profile.educations = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
        datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
        now = dt.datetime.now()
        if datetime_object > now:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
        else:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
        for education in educations:
            credential = dict()
            credential["ID"] = education.umeta_id
            current_education = json.loads(education.meta_value)
            school = current_education["school"]
            credential["school"] = school
            major = current_education["major"]
            credential["major"] = major
            credential["minor"] = current_education["minor"]
            degree = current_education["degree"]
            credential["degree"] = degree
            graduation = current_education["graduation"]
            credential["graduation"] = graduation
            cred = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
            datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
            else:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
            credential["cred"] = cred
            profile.education_credentials.append(credential)

    
    locations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'locations').order_by('-umeta_id')
    profile.location_credentials = []
    if locations.count() > 0:
        current_location = json.loads(locations[0].meta_value)
        location = current_location["location"]
        startDate = current_location["startDate"]
        endDate = current_location["endDate"]
        if endDate == "current":
            profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
        else:
            datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                profile.locations = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
        for location in locations:
            credential = dict()
            credential["ID"] = location.umeta_id
            current_location = json.loads(location.meta_value)
            location = current_location["location"]
            credential["location"] = location
            startDate = current_location["startDate"]
            credential["startDate"] = startDate
            endDate = current_location["endDate"]
            credential["endDate"] = endDate
            if endDate == "current":
                cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
                now = dt.datetime.now()
                if datetime_object > now:
                    cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
                else:
                    cred = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
            credential["cred"] = cred
            profile.location_credentials.append(credential)

    
    languages = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'languages').order_by('-umeta_id')
    profile.language_credentials = []
    if languages.count() > 0:
        current_language = json.loads(languages[0].meta_value)
        language = current_language["language"]
        language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
        language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
        profile.languages = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
        for l in languages:
            credential = dict()
            credential["ID"] = l.umeta_id
            current_language = json.loads(l.meta_value)
            language = current_language["language"]
            credential["language"] = language
            language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
            language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
            cred = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
            credential["cred"] = cred
            profile.language_credentials.append(credential)
    
    photos = PostMeta.objects.filter(meta_key="media_type", meta_value="image")
    photos = list({x.post_id: x for x in photos}.keys())
    medias = Post.objects.filter(ID__in=photos, post_author=profile.ID, post_status="publish", post_type="media").order_by('-post_date')[:6]
    for media in medias:
        setup_postmeta(media, word_list)
        setup_mediameta(media)
    empty_medias = 6 - medias.count()
    followers = UserRelation.objects.filter(following=profile)
    for follower in followers:
        try:
            follower.follower = setup_current_user(follower.follower.ID)
        except:
            follower.delete()
    followers = UserRelation.objects.filter(following=profile)
    for follower in followers:
        follower.follower = setup_current_user(follower.follower.ID)
    suggesteds = get_suggested_users(word_list, current_user)
    if len(suggesteds) == 0:
        suggesteds.extend(get_suggested_users2(current_uid))
        for user in suggesteds:
            user.avatar_url = setup_avatar_url(user.ID)
    return render(request, 'users/followers.html', {'current_user':current_user, 'lang':lang, 'darkmode':dark, 'dark':dark, 'word_list':word_list, 
                                            'profile':profile, 'country_list':country_list, 'medias':medias,
                                            'empty_medias':range(empty_medias), 'followers':followers, 'followtxt':followtxt, 'followingtxt':followingtxt,
                                            'users':suggesteds
                                            })

def userfollowings(request, username):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    profile = setup_current_user(User.objects.filter(user_login=username)[0].ID)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for f in profile.followers:
        f.follower.avatar_url = setup_avatar_url(f.follower.ID)
    employments = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'employments').order_by('-umeta_id')
    profile.employment_credentials = []
    if employments.count() > 0:
        current_employment = json.loads(employments[0].meta_value)
        position = current_employment["position"]
        company = current_employment["company"]
        profile.employments = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
        for employment in employments:
            credential = dict()
            credential["ID"] = employment.umeta_id
            current_employment = json.loads(employment.meta_value)
            position = current_employment["position"]
            credential["position"] = position
            credential["startDate"] = current_employment["startDate"]
            credential["endDate"] = current_employment["endDate"]
            company = current_employment["company"]
            credential["company"] = company
            cred = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
            credential["cred"] = cred
            profile.employment_credentials.append(credential)
    
    educations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'educations').order_by('-umeta_id')
    profile.education_credentials = []
    if educations.count() > 0:
        current_education = json.loads(educations[0].meta_value)
        school = current_education["school"]
        major = current_education["major"]
        degree = current_education["degree"]
        graduation = current_education["graduation"]
        profile.educations = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
        datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
        now = dt.datetime.now()
        if datetime_object > now:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
        else:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
        for education in educations:
            credential = dict()
            credential["ID"] = education.umeta_id
            current_education = json.loads(education.meta_value)
            school = current_education["school"]
            credential["school"] = school
            major = current_education["major"]
            credential["major"] = major
            credential["minor"] = current_education["minor"]
            degree = current_education["degree"]
            credential["degree"] = degree
            graduation = current_education["graduation"]
            credential["graduation"] = graduation
            cred = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
            datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
            else:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
            credential["cred"] = cred
            profile.education_credentials.append(credential)

    
    locations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'locations').order_by('-umeta_id')
    profile.location_credentials = []
    if locations.count() > 0:
        current_location = json.loads(locations[0].meta_value)
        location = current_location["location"]
        startDate = current_location["startDate"]
        endDate = current_location["endDate"]
        if endDate == "current":
            profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
        else:
            datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                profile.locations = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
        for location in locations:
            credential = dict()
            credential["ID"] = location.umeta_id
            current_location = json.loads(location.meta_value)
            location = current_location["location"]
            credential["location"] = location
            startDate = current_location["startDate"]
            credential["startDate"] = startDate
            endDate = current_location["endDate"]
            credential["endDate"] = endDate
            if endDate == "current":
                cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
                now = dt.datetime.now()
                if datetime_object > now:
                    cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
                else:
                    cred = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
            credential["cred"] = cred
            profile.location_credentials.append(credential)

    
    languages = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'languages').order_by('-umeta_id')
    profile.language_credentials = []
    if languages.count() > 0:
        current_language = json.loads(languages[0].meta_value)
        language = current_language["language"]
        language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
        language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
        profile.languages = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
        for l in languages:
            credential = dict()
            credential["ID"] = l.umeta_id
            current_language = json.loads(l.meta_value)
            language = current_language["language"]
            credential["language"] = language
            language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
            language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
            cred = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
            credential["cred"] = cred
            profile.language_credentials.append(credential)
    
    photos = PostMeta.objects.filter(meta_key="media_type", meta_value="image")
    photos = list({x.post_id: x for x in photos}.keys())
    medias = Post.objects.filter(ID__in=photos, post_author=profile.ID, post_status="publish", post_type="media").order_by('-post_date')[:6]
    for media in medias:
        setup_postmeta(media, word_list)
        setup_mediameta(media)
    empty_medias = 6 - medias.count()
    followings = UserRelation.objects.filter(follower=profile)
    for following in followings:
        try:
            following.following = setup_current_user(following.following.ID)
        except:
            following.delete()
    followings = UserRelation.objects.filter(follower=profile)
    for following in followings:
        following.following = setup_current_user(following.following.ID)
    suggesteds = get_suggested_users(word_list, current_user)
    if len(suggesteds) == 0:
        suggesteds.extend(get_suggested_users2(current_uid))
        for user in suggesteds:
            user.avatar_url = setup_avatar_url(user.ID)
    return render(request, 'users/followings.html', {'current_user':current_user, 'lang':lang, 'darkmode':dark, 'dark':dark, 'word_list':word_list, 
                                            'profile':profile, 'country_list':country_list, 'medias':medias,
                                            'empty_medias':range(empty_medias), 'followings':followings, 'followtxt':followtxt, 'followingtxt':followingtxt,
                                            'users':suggesteds
                                            })

def usersuggested(request, username):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    profile = setup_current_user(User.objects.filter(user_login=username)[0].ID)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    for f in profile.followers:
        f.follower.avatar_url = setup_avatar_url(f.follower.ID)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    employments = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'employments').order_by('-umeta_id')
    profile.employment_credentials = []
    if employments.count() > 0:
        current_employment = json.loads(employments[0].meta_value)
        position = current_employment["position"]
        company = current_employment["company"]
        profile.employments = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
        for employment in employments:
            credential = dict()
            credential["ID"] = employment.umeta_id
            current_employment = json.loads(employment.meta_value)
            position = current_employment["position"]
            credential["position"] = position
            credential["startDate"] = current_employment["startDate"]
            credential["endDate"] = current_employment["endDate"]
            company = current_employment["company"]
            credential["company"] = company
            cred = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
            credential["cred"] = cred
            profile.employment_credentials.append(credential)
    
    educations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'educations').order_by('-umeta_id')
    profile.education_credentials = []
    if educations.count() > 0:
        current_education = json.loads(educations[0].meta_value)
        school = current_education["school"]
        major = current_education["major"]
        degree = current_education["degree"]
        graduation = current_education["graduation"]
        profile.educations = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
        datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
        now = dt.datetime.now()
        if datetime_object > now:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
        else:
            profile.educations = profile.educations + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
        for education in educations:
            credential = dict()
            credential["ID"] = education.umeta_id
            current_education = json.loads(education.meta_value)
            school = current_education["school"]
            credential["school"] = school
            major = current_education["major"]
            credential["major"] = major
            credential["minor"] = current_education["minor"]
            degree = current_education["degree"]
            credential["degree"] = degree
            graduation = current_education["graduation"]
            credential["graduation"] = graduation
            cred = word_list.filter(var_name="education-string")[0].translation.replace("{degree}", degree).replace("{major}",major).replace("{school}", school)
            datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="expected-graduation")[0].translation + ": "+graduation[0:4]+"</span>"
            else:
                cred = cred + "<span class='cg fwlight'> " + word_list.filter(var_name="graduated-at")[0].translation.replace("{year}", graduation[0:4])+"</span>"
            credential["cred"] = cred
            profile.education_credentials.append(credential)

    
    locations = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'locations').order_by('-umeta_id')
    profile.location_credentials = []
    if locations.count() > 0:
        current_location = json.loads(locations[0].meta_value)
        location = current_location["location"]
        startDate = current_location["startDate"]
        endDate = current_location["endDate"]
        if endDate == "current":
            profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
        else:
            datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                profile.locations = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
        for location in locations:
            credential = dict()
            credential["ID"] = location.umeta_id
            current_location = json.loads(location.meta_value)
            location = current_location["location"]
            credential["location"] = location
            startDate = current_location["startDate"]
            credential["startDate"] = startDate
            endDate = current_location["endDate"]
            credential["endDate"] = endDate
            if endDate == "current":
                cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                datetime_object = dt.datetime.strptime(endDate, '%Y-%m')
                now = dt.datetime.now()
                if datetime_object > now:
                    cred = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
                else:
                    cred = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
            credential["cred"] = cred
            profile.location_credentials.append(credential)

    
    languages = UserMeta.objects.filter(user_id = profile.ID, meta_key = 'languages').order_by('-umeta_id')
    profile.language_credentials = []
    if languages.count() > 0:
        current_language = json.loads(languages[0].meta_value)
        language = current_language["language"]
        language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
        language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
        profile.languages = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
        for l in languages:
            credential = dict()
            credential["ID"] = l.umeta_id
            current_language = json.loads(l.meta_value)
            language = current_language["language"]
            credential["language"] = language
            language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
            language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
            cred = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
            credential["cred"] = cred
            profile.language_credentials.append(credential)
    
    photos = PostMeta.objects.filter(meta_key="media_type", meta_value="image")
    photos = list({x.post_id: x for x in photos}.keys())
    medias = Post.objects.filter(ID__in=photos, post_author=profile.ID, post_status="publish", post_type="media").order_by('-post_date')[:6]
    for media in medias:
        setup_postmeta(media, word_list)
        setup_mediameta(media)
    empty_medias = 6 - medias.count()
    suggesteds = []
    visitor_followings_ids = list({x.following_id: x for x in current_user.followings}.keys())
    if profile.ID != current_uid:
        common_followings = UserRelation.objects.filter(following_id__in=visitor_followings_ids, follower=profile)
        common_followings_ids = list({x.following_id: x for x in common_followings}.keys())
        common_followers = UserRelation.objects.filter(follower_id__in=visitor_followings_ids, following=profile)
        common_followers_ids = list({x.follower_id: x for x in common_followers}.keys())
        common_ids = common_followings_ids + common_followers_ids
        common_ids = list(dict.fromkeys(common_ids))
        follower_relations = UserRelation.objects.filter(follower_id__in=common_ids)
        follower_relations_ids = list({x.following_id: x for x in follower_relations}.keys())
        following_relations = UserRelation.objects.filter(following_id__in=common_ids)
        following_relations_ids = list({x.follower_id: x for x in following_relations}.keys())
        relations_ids = follower_relations_ids + following_relations_ids
        relations_ids = list(dict.fromkeys(relations_ids))
        suggested_followers = UserRelation.objects.filter(follower_id__in=relations_ids, following=profile)
        suggested_followers_ids = list({x.follower_id: x for x in suggested_followers}.keys())
        suggested_followings = UserRelation.objects.filter(following_id__in=relations_ids, follower=profile)
        suggested_followings_ids = list({x.following_id: x for x in suggested_followings}.keys())
        suggested_ids = suggested_followers_ids + suggested_followings_ids
        suggested_ids = list(dict.fromkeys(suggested_ids))
        for sid in suggested_ids:
            isFollowed = UserRelation.objects.filter(following_id=sid, follower=current_user)
            if isFollowed.count() == 0 and sid != current_uid:
                user = setup_current_user(sid)
                suggesteds.append(user)
    suggestion_dict = dict()
    for vid in visitor_followings_ids:
        followings = UserRelation.objects.filter(follower_id=vid)
        followings_ids = list({x.following_id: x for x in followings}.keys())
        for fid in followings_ids:
            if fid in suggestion_dict:
                suggestion_dict[fid] = suggestion_dict[fid] + 1
            else:
                suggestion_dict[fid] = 1
    #suggestion_dict = {k: v for k, v in suggestion_dict.items() if v >= 2}
    for (k, _) in suggestion_dict.items():
        isFollowed = UserRelation.objects.filter(following_id=k, follower=current_user)
        if isFollowed.count() == 0 and k != current_uid and k != profile.ID:
            try:
                user = setup_current_user(k)
                if user not in suggesteds:
                    suggesteds.append(user)
            except:
                pass
    for suggested in suggesteds:
        relative_users = UserRelation.objects.filter(following=suggested, follower_id__in=visitor_followings_ids)
        relative_usernames = list({"u/"+x.follower.user_login: x for x in relative_users}.keys())
        and_string = word_list.filter(var_name="and")[0].translation
        people_string = ""
        if len(relative_usernames) == 1:
            people_string = relative_usernames[0]
        elif len(relative_usernames) == 2:
            people_string = relative_usernames[0] + " " + and_string + " " + relative_usernames[1]
        else:
            people_string = ", ".join(relative_usernames[0:2]) + " " + and_string + " " + str(len(relative_usernames) - 2) + " " + word_list.filter(var_name="more-users")[0].translation
        suggested.relatives = word_list.filter(var_name="relative_followers_string")[0].translation.replace("{user}", people_string)
    if len(suggesteds) == 0:
        suggesteds.extend(get_suggested_users2(current_uid))
        for user in suggesteds:
            user.avatar_url = setup_avatar_url(user.ID)
    return render(request, 'users/suggested.html', {'current_user':current_user, 'lang':lang, 'darkmode':dark, 'dark':dark, 'word_list':word_list, 
                                            'profile':profile, 'country_list':country_list, 'medias':medias,
                                            'empty_medias':range(empty_medias), 'suggesteds': suggesteds, 'followtxt':followtxt, 'followingtxt':followingtxt
                                            })

def notifications(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if 'filter' in kwargs:
        fltr = kwargs.get("filter").split("_")[0]
    else:
        fltr = "all"
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, _ = setup_notifications(current_uid, word_list, filter=fltr)
    return render(request, 'notifications.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'filter':fltr
                                            })

def questions(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    page = "questions"
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    title = fun.ucfirst(word_list.filter(var_name="questions")[0].translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    followed_communities = FollowedCommunities.objects.filter(user=current_user)
    question_ids = []
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    for comm in followed_communities:
        community = comm.term
        taxonomy = TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
        post_ids = TermRelationship.objects.filter(Q(term_taxonomy_id=taxonomy))
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        question_ids += post_ids
    questions = Post.objects.filter(ID__in=question_ids, post_type="questions").order_by('-post_date')
    for question in questions:
        community_taxonomy_ids = TermRelationship.objects.filter(object_id=question.ID)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        question.communities = Community.objects.filter(term_id__in=community_ids)
        if question.communities.count() > 0:
            question.first_community = question.communities[0].name
        isfollowed = FollowedPosts.objects.filter(post=question, user=current_user, following=1)
        if isfollowed.count() > 0:
            question.isfollowed = 1
        question.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=question.ID)
        setup_postmeta(question, word_list)
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    suggesteds = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'questions.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'page':page, 'questions': questions, 'user_list':user_list, 'title': title,
                                            'popular_communities':popular_communities, 'users':suggesteds
                                            })

def answerrequests(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    title = fun.ucfirst(word_list.filter(var_name="questions")[0].translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    followed_communities = FollowedCommunities.objects.filter(user=current_user)
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    questions = PostRequest.objects.filter(receiver_id=current_uid, answered=0, post_type="answer").order_by("-date")
    for question in questions:
        question.sender = setup_current_user(question.sender_id)
        isfollowed = FollowedPosts.objects.filter(post=question.post, user=current_user, following=1)
        if isfollowed.count() > 0:
            question.post.isfollowed = 1
        question.post.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=question.post.ID)
        setup_postmeta(question.post, word_list)
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    suggesteds = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'answerrequests.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'questions': questions, 'user_list':user_list, 'title': title, 'popular_communities':popular_communities,
                                            'users':suggesteds
                                            })

def answerdrafts(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    title = fun.ucfirst(word_list.filter(var_name="questions")[0].translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    followed_communities = FollowedCommunities.objects.filter(user=current_user)
    question_ids = []
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    questions = Post.objects.filter(post_author=current_uid, post_type="answer", post_status="draft").order_by('-post_date')
    for question in questions:
        isfollowed = FollowedPosts.objects.filter(post=question, user=current_user, following=1)
        if isfollowed.count() > 0:
            question.isfollowed = 1
        question.answers = Post.objects.filter(post_type="answer", post_status="publish", post_parent=question.ID)
        setup_postmeta(question, word_list)
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    suggesteds = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'answerdrafts.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'questions': questions, 'user_list':user_list, 'title': title,
                                            'popular_communities':popular_communities, 'users':suggesteds
                                            })

def quizzes(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    page = "quizzes"
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    try:
        fromcompage = request.GET["fromcompage"]
        if fromcompage == "yes":
            return quizzesfiltered(request, filter=fltr)
    except:
        pass
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    title = fun.ucfirst(word_list.get(var_name = 'quizzes').translation)
    categories = CommunityCategories.objects.all()
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    quizzes = Post.objects.filter(post_type="quiz", post_status="publish").order_by("-post_date")
    if fltr != "all":
        selected_category = CommunityCategories.objects.get(slug=fun.localized_upper(fltr))
        community_list = CommunityCategoryRelation.objects.filter(category=selected_category)
        community_ids = list({x.community_id: x for x in community_list}.keys())
        taxonomies = TermTaxonomy.objects.filter(term_id__in=community_ids)
        taxonomy_ids = list({x.term_taxonomy_id: x for x in taxonomies}.keys())
        post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomy_ids)
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        quizzes = quizzes.filter(ID__in=post_ids)
    for post in quizzes:
        setup_postmeta(post, word_list)
        post.quiz_type = PostMeta.objects.filter(post_id=post.ID, meta_key="quiz_type")[0].meta_value
        post.post_title = post.post_title.replace(" - Sosyorol", "")
        if post.quiz_type == "media":
            setup_media_quizmeta(post, word_list)
        elif post.quiz_type == "colorBox":
            setup_colorbox_quizmeta(post, word_list)
        else:
            setup_quizmeta(post, word_list)
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    users = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'quizzes.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'page':page, 'title':title, 'categories':categories, 'quizzes':quizzes, 'user_list':user_list,
                                            'filter':fltr, 'popular_communities':popular_communities, 'users':users
                                            })

def polls(request, **kwargs):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    page = "polls"
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    try:
        fromcompage = request.GET["fromcompage"]
        if fromcompage == "yes":
            return pollsfiltered(request, filter=fltr)
    except:
        pass
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    title = fun.ucfirst(word_list.get(var_name = 'polls').translation)
    categories = CommunityCategories.objects.all()
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    polls = Post.objects.filter(post_type="poll", post_status="publish").order_by("-post_date")
    if fltr != "all":
        selected_category = CommunityCategories.objects.get(slug=fun.localized_upper(fltr))
        community_list = CommunityCategoryRelation.objects.filter(category=selected_category)
        community_ids = list({x.community_id: x for x in community_list}.keys())
        taxonomies = TermTaxonomy.objects.filter(term_id__in=community_ids)
        taxonomy_ids = list({x.term_taxonomy_id: x for x in taxonomies}.keys())
        post_ids = TermRelationship.objects.filter(term_taxonomy_id__in=taxonomy_ids)
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        polls = polls.filter(ID__in=post_ids)
    for post in polls:
        setup_postmeta(post, word_list)
        community_taxonomy_ids = TermRelationship.objects.filter(Q(object_id=post.ID))
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        post.communities = Community.objects.filter(term_id__in=community_ids)
        if post.communities.count() > 0:
            post.first_community = post.communities[0].name
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    suggesteds = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'polls.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'page':page, 'title':title, 'categories':categories, 'polls':polls, 'user_list':user_list,
                                            'filter':fltr, 'popular_communities':popular_communities, "users":suggesteds
                                            })

def quizrequests(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    title = fun.ucfirst(word_list.get(var_name = 'quizzes').translation)
    categories = CommunityCategories.objects.all()
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    quizzes = PostRequest.objects.filter(receiver_id=current_uid, answered=0, post_type="quiz").order_by("-date")
    for quiz in quizzes:
        quiz.sender = setup_current_user(quiz.sender_id)
        setup_postmeta(quiz.post, word_list)
        quiz.post.quiz_type = PostMeta.objects.filter(post_id=quiz.post.ID, meta_key="quiz_type")[0].meta_value
        quiz.post.post_title = quiz.post.post_title.replace(" - Sosyorol", "")
        if quiz.post.quiz_type == "media":
            setup_media_quizmeta(quiz.post, word_list)
        elif quiz.post.quiz_type == "colorBox":
            setup_colorbox_quizmeta(quiz.post, word_list)
        else:
            setup_quizmeta(quiz.post, word_list)
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    suggesteds = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'quizrequests.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'title':title, 'categories':categories, 'quizzes':quizzes, 'user_list':user_list,
                                            'popular_communities':popular_communities, 'users':suggesteds
                                            })

def pollrequests(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    import random
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    title = fun.ucfirst(word_list.get(var_name = 'polls').translation)
    categories = CommunityCategories.objects.all()
    user_list = []
    for user in current_user.followings:
        user = setup_current_user(user.following_id)
        user_list.append(user)
    random.shuffle(user_list)
    polls = PostRequest.objects.filter(receiver_id=current_uid, answered=0, post_type="poll").order_by("-date")
    for poll in polls:
        poll.sender = setup_current_user(poll.sender_id)
        setup_postmeta(poll.post, word_list)
        community_taxonomy_ids = TermRelationship.objects.filter(object_id=poll.post.ID)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids}.keys())
        poll.post.communities = Community.objects.filter(term_id__in=community_ids)
        if poll.post.communities.count() > 0:
            poll.post.first_community = poll.post.communities[0].name
    popular_communities = TermTaxonomy.objects.filter(taxonomy="post_tag").order_by('-count')[:5].prefetch_related()
    suggesteds = get_suggested_users(word_list, current_user)[:4]
    return render(request, 'pollrequests.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'title':title, 'categories':categories, 'polls':polls, 'user_list':user_list,
                                            'popular_communities':popular_communities, 'users':suggesteds
                                            })

def chat(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    sosmojis = os.listdir(os.path.join(STATICFILES_DIR, "assets/img/sosmojis/"))
    return render(request, 'chat.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'sosmojis':sosmojis})

def chatdetail(request, chat_id):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    sosmojis = os.listdir(os.path.join(STATICFILES_DIR, "assets/img/sosmojis/"))
    return render(request, 'chatdetail.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'sosmojis':sosmojis})

def settings(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    return render(request, 'settings.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications})

def privacysettings(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    try:
        phone_privacy_setting = UserMeta.objects.filter(user_id=current_uid, meta_key="phone_privacy_setting")[0].meta_value
    except:
        phone_privacy_setting = "everyone"
    try:
        email_privacy_setting = UserMeta.objects.filter(user_id=current_uid, meta_key="email_privacy_setting")[0].meta_value
    except:
        email_privacy_setting = "everyone"
    try:
        location_privacy_setting = UserMeta.objects.filter(user_id=current_uid, meta_key="location_privacy_setting")[0].meta_value
    except:
        location_privacy_setting = "everyone"
    return render(request, 'privacy_settings.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'phone_privacy_setting':phone_privacy_setting, 'email_privacy_setting':email_privacy_setting,
                                            'location_privacy_setting':location_privacy_setting})

def notificationsettings(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    try:
        comment_notif = int(UserMeta.objects.filter(user_id=current_uid, meta_key="comment_notif_setting")[0].meta_value)
    except:
        comment_notif = 1
    try:
        answer_notif = int(UserMeta.objects.filter(user_id=current_uid, meta_key="answer_notif_setting")[0].meta_value)
    except:
        answer_notif = 1
    try:
        post_notif_comm = int(UserMeta.objects.filter(user_id=current_uid, meta_key="post_notif_comm_setting")[0].meta_value)
    except:
        post_notif_comm = 1
    try:
        post_notif_following = int(UserMeta.objects.filter(user_id=current_uid, meta_key="post_notif_following_setting")[0].meta_value)
    except:
        post_notif_following = 1
    try:
        following_notif = int(UserMeta.objects.filter(user_id=current_uid, meta_key="following_notif_setting")[0].meta_value)
    except:
        following_notif = 1
    try:
        birthday_notif = int(UserMeta.objects.filter(user_id=current_uid, meta_key="birthday_notif_setting")[0].meta_value)
    except:
        birthday_notif = 1
    return render(request, 'notification_settings.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'comment_notif':comment_notif, 'answer_notif':answer_notif, 'post_notif_comm':post_notif_comm,
                                            'post_notif_following':post_notif_following, 'following_notif':following_notif, 'birthday_notif':birthday_notif})

def chatsettings(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    try:
        chat_preference = UserMeta.objects.filter(user_id=current_uid, meta_key="chat_preference")[0].meta_value
    except:
        chat_preference = "everyone"
    return render(request, 'chat_settings.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'chat_preference': chat_preference})

def feedsettings(request):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    try:
        nsfw = int(UserMeta.objects.filter(user_id=current_uid, meta_key="nsfw_preference")[0].meta_value)
    except:
        nsfw = 0
    return render(request, 'feed_settings.html', {'lang':lang, 'darkmode':dark, 'dark':dark, 'current_user': current_user,
                                            'country_list':country_list, 'select_language':select_language,
                                            'word_list':word_list, 'notifications':notifications, 'num_notifications':num_notifications,
                                            'nsfw':nsfw})

def commentdetail(request, username, comment_id):
    current_uid = get_current_uid(request)
    if current_uid == -1:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    ref = ""
    try:
        ref = request.GET["ref"]
    except:
        pass
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(user_id = current_uid).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(lang_code = lang)
    commentid = int(comment_id.replace("c", "x"), 16) - 100000
    comment = Comment.objects.filter(comment_ID=commentid)[0]
    comment.user = setup_current_user(comment.user.ID)
    comment.comment_post.author = setup_current_user(comment.comment_post.post_author)
    comment.comment_post.post_title = comment.comment_post.post_title.replace(" - Sosyorol", "")
    comment.child_comments = Comment.objects.none()
    comment.child_comments = getchildcomments(comment.comment_post.ID, comment.comment_ID)
    getgrandchildcomments(comment.comment_post.ID, comment.child_comments)
    comment.comment_post.hex_id = hex(comment.comment_post.ID + 100000).replace("x", "s")
    comment.comment_post.post_title = comment.comment_post.post_title.replace(" - Sosyorol", "")
    comment.comment_post.guid = arrange_post_slug(comment.comment_post.post_title)
    notifications, num_notifications = setup_notifications(current_uid, word_list)
    followtxt = word_list.filter(var_name="follow")[0].translation
    followingtxt = word_list.filter(var_name="following")[0].translation
    more_from_content_owner = word_list.filter(var_name="more_from_content_owner")[0].translation
    more_from_content_owner = more_from_content_owner.replace("{user}", "<a class='fs19 title ctitle underline-on-hover' href='/u/"+comment.user.user_login+"'>"+comment.user.user_login+"</a>")
    other_comments = Comment.objects.filter(user=comment.user).exclude(comment_ID=commentid).order_by("-comment_date")[:3]
    for op in other_comments:
        op.hex_id = hex(op.comment_ID + 100000).replace("x", "c")
    return render(request, "commentdetail.html", {'comment':comment, 'ref':ref, 'current_user':current_user, 
                                                    'lang':lang, 'darkmode':dark, 'dark':dark, 'word_list':word_list, 'notifications':notifications,
                                                    'num_notifications':num_notifications, 'followtxt':followtxt, 'followingtxt':followingtxt,
                                                    'more_from_content_owner':more_from_content_owner, 'other_comments':other_comments})