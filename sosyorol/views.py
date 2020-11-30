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
import firebase_admin
from firebase_admin import auth, credentials, exceptions
from itertools import chain
from django.views.generic.list import ListView

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
    header_dict['createpost'] = word_list.get(var_name = 'create-post').translation
    header_dict['profile'] = word_list.get(var_name = 'profile').translation
    header_dict['messages'] = word_list.get(var_name = 'messages').translation
    header_dict['notifications'] = word_list.get(var_name = 'notifications').translation
    return header_dict

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
    page_dict["notmatchingpasserror"] = word_list.filter(Q(var_name = 'not-matching-pass-error'))[0].translation
    return page_dict

def  search_page_dict(word_list):
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
def arrange_post_slug(title):
    import string
    title = title.lower()
    title = title.replace("ı","i")
    title = title.replace("ç","c")
    title = title.replace("ş","s")
    title = title.replace("ö","o")
    title = title.replace("ü","u")
    title = title.replace("ğ","g")
    title = title.translate(str.maketrans('', '', string.punctuation))
    title = title.replace(' ','_')
    return title

def setup_quizmeta(post, word_list):
    import re
    current_uid = 8
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
    current_uid = 8
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
    isvoted = SossyComments.objects.filter(post_id=post.ID, user_id=current_uid)
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
            post.poll_duration_left = "bitti"   

def setup_mediameta(post):
    post.media_type = PostMeta.objects.filter(post_id=post.ID, meta_key="media_type")[0].meta_value
    post.media_url = PostMeta.objects.filter(post_id=post.ID, meta_key="media_url")[0].meta_value

def setup_postmeta(post, word_list):
    import re
    current_uid = 8
    post.hex_id = hex(post.ID + 100000).replace("x", "s")
    post.post_title = post.post_title.replace(" - Sosyorol", "")
    post.guid = arrange_post_slug(post.post_title)
    post.like = PostRating.objects.filter(post_id=post.ID, opinion='like').count()
    post.dislike = PostRating.objects.filter(post_id=post.ID, opinion='dislike').count()
    post.rating = post.like - post.dislike
    post.repost = Repost.objects.filter(post_id=post.ID).count()

    community_taxonomy_ids = TermRelationship.objects.filter(Q(object_id=post.ID))
    community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
    community_ids = TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
    community_ids = list({x.term_id: x for x in community_ids}.keys())
    post.communities = Community.objects.filter(term_id__in=community_ids)
    if post.communities.count() > 0:
        post.first_community = post.communities[0].name

    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{post.author_id}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(post.author_id) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    post.author.set_avatar(avatar_url)
    post.time_diff = fun.humanizedate(post.post_date.replace(tzinfo=None), word_list)

    if post.post_type == "answer":
        post.parent = Post.objects.filter(ID=post.post_parent)[0]
        post.parent.guid = arrange_post_slug(post.parent.post_title)
        post.parent.hex_id = hex(post.parent.ID + 100000).replace("x", "s")
    
    if post.post_type == "post" or post.post_type == "answer":
        soup = BSHTML(post.post_content,features="html.parser")
        images = soup.findAll('img')
        post.post_images = []
        featured_img = PostMeta.objects.filter(post_id=post.ID, meta_key="_thumbnail_id")
        if featured_img.count() > 0:
            featured_id = featured_img[0].meta_value
            featured_img = Post.objects.get(ID=featured_id).guid
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
    
    post.comments = Comment.objects.filter(comment_post_ID=post.ID)
    if post.post_type == "answer":
        if (post.post_parent == 0):
            post.parent_title = post.post_title
        else:
            post.parent_title = Post.objects.get(ID=post.post_parent).post_title

    israted = PostRating.objects.filter(post_id=post.ID, user_id=current_uid)
    if israted.count() > 0:
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

def morecommunities(request):
    print("loadmoreleaderboardcommunities")
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
    
    print(hasMore)
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
        
def setup_current_user(current_uid):
    current_user = User.objects.get(ID = current_uid)
    user_desc = UserMeta.objects.filter(user_id = current_uid, meta_key = 'description')[0]
    current_user.description = user_desc.meta_value
    current_user.posts = Post.objects.filter(post_author=current_uid, post_status="publish", post_type__in=["post","quiz","media","link","questions","answer"]).order_by('-post_date')
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    if (os.path.exists(mypath)):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    else:
        avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    current_user.avatar_url = avatar_url
    try:
        current_user.followers = UserRelation.objects.filter(following=current_user)
        current_user.followings = UserRelation.objects.filter(follower=current_user)
        for f in current_user.followers:
            try:
                mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{f.follower.ID}')
                if (os.path.exists(mypath)):
                    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                    avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(f.follower.ID) + "/" + onlyfiles[0]
                else:
                    avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
                f.follower.avatar_url = avatar_url
            except:
                f.follower.avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
    except:
        pass
    return current_user

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
        selected_category = CommunityCategories.objects.get(name=fun.localized_upper(fltr))
        community_list = CommunityCategoryRelation.objects.filter(category=selected_category)[:20]
    return render(request, 'communities/communitytemplates/leaderboard.html', {'communities':community_list, 'filter':fltr})

def addanotherquizresult(request):
    nmr = str(int(request.GET["number"]) + 1)
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    return render(request, 'posts/createpost/quiz_result.html', {'number':nmr, 'word_list':word_list})

def addanotherquizquestion(request):
    nmr = str(int(request.GET["number"]) + 1)
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    qtype = request.GET["type"]
    return render(request, 'posts/createpost/quiz_question.html', {'number':nmr, 'word_list':word_list, 'qtype':qtype})

def getchildcomments(post_id, parent_id):
    comments = Comment.objects.filter(comment_post_ID=post_id, comment_parent=parent_id).order_by('-comment_date').prefetch_related()
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
        print(offset)
        print(limit)
        comments = Comment.objects.filter(comment_post_ID=post_id, comment_parent=parent_id).order_by('-comment_date').prefetch_related()
        comments = comments[offset:(offset + limit)]
        print(comments)
        current_uid = 8
        current_user = setup_current_user(current_uid)
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
        for comment in comments:
            comment.user = setup_current_user(comment.user.ID)
            comment.child_comments = Comment.objects.none()
            comment.child_comments = getchildcomments(post_id, comment.comment_ID)
            getgrandchildcomments(post_id, comment.child_comments)
        print(comments)
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
        print(fltr)
        hasMore = "True"
        if fltr == "all" or flter == "":
            moreposts = Post.objects.filter(post_author=user_id, post_status="publish", post_type__in=["post","quiz","media","link","questions","answer"]).order_by('-post_date')
            if moreposts.count() < offset :
                hasMore = "False"
            elif moreposts.count() < offset + limit:
                moreposts = moreposts[offset:]
                hasMore = "False"
            else:
                moreposts = moreposts[offset:(offset + limit)]
        else:
            if fltr == "question":
                fltr = "questions"
            moreposts = Post.objects.filter(post_author=user_id, post_status="publish", post_type=fltr).order_by('-post_date')
            if moreposts.count() < offset :
                hasMore = "False"
            elif moreposts.count() < offset + limit:
                moreposts = moreposts[offset:]
                hasMore = "False"
            else:
                moreposts = moreposts[offset:(offset + limit)]
        current_uid = 8
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
        if fltr == "questions":
            fltr = "question"
        return render(request, 'posts/loadmoreposts.html', {'moreposts':moreposts, 'word_list':word_list, 'fltr':fltr, 'offset':offset, 'hasMore':hasMore, 'current_user':current_user})
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")

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
def uploadmediagetcolor(request):
    from sosyorol.forms import MediaFileUploadForm
    from colorthief import ColorThief
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
            response_data[result.guid] = "post!:!" +result.post_title
    if (result_count < 6):
        diff = 6 - result_count
        results = User.objects.filter(Q(display_name__icontains=search_key))[:diff]
        for result in results:
            result = setup_current_user(result.ID)
            response_data[result.user_nicename] = "user!:!" + result.avatar_url + "!:!" + result.display_name
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def getlanguages(request):
    search_key = request.GET["search"]
    current_uid = 8
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    response_data = {}
    results = Languages.objects.filter(lang_code=lang, var_name__icontains="lang-ns-", translation__icontains=search_key)
    for result in results:
        response_data[result.var_name] = "lang!:!" +result.translation
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def savenewquiz(request):
    import re
    current_uid = 8
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

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.filter(term=term)[0]
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()

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

    response_data = {}
    response_data['content'] = "success"                        
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewpost(request):
    import re
    current_uid = 8
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

    for (k, v) in communities.items():
        term = Community.objects.get(name=str(v))
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()

    response_data = {}
    response_data['content'] = "success"                        
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewmediapost(request):
    current_uid = 8
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

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()

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

    response_data = {}
    response_data['content'] = "success"                   
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewlink(request):
    current_uid = 8
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

    for (k, v) in communities.items():
        term = Community.objects.get(name=str(v))
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()

    post_url = PostMeta(post_id=new_quiz.ID, meta_key="post_url", meta_value=post_url)
    post_url.save()

    response_data = {}
    response_data['content'] = "success"                   
    return HttpResponse(json.dumps(response_data),content_type="application/json")
@csrf_exempt
def savenewquestion(request):
    import re
    current_uid = 8
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
    new_quiz = Post(post_title=quiz_title, post_content=quiz_desc, post_date=dt.datetime.now(), author=current_user, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="question", post_excerpt=post_excerpt, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    for (k, v) in communities.items():
        term = Community.objects.get(name=str(v))
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()

    for (k, v) in flairs.items():
        tokens = str(v).replace("&nbsp;", "").split("--")
        flair = tokens[0]
        community =  Community.objects.get(name=tokens[1])
        flr = Flairs.objects.filter(flair=flair, term_id=community.term_id)[0]
        new_flair = PostFlair(post_id=new_quiz.ID, flair=flr)
        new_flair.save()

    post_url = PostMeta(post_id=new_quiz.ID, meta_key="post_url", meta_value=post_url)
    post_url.save()

    response_data = {}
    response_data['content'] = "success"                   
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewpoll(request):
    import re
    current_uid = 8
    quiz_title = request.POST["post_title"]
    communities = json.loads(request.POST['communities'])
    flairs = json.loads(request.POST['flairs'])
    options = json.loads(request.POST['poll_options'])
    quiz_desc = request.POST["post_content"]
    poll_duration = request.POST["poll_duration"]

    post_excerpt = re.sub("(<img.*?>)", "", quiz_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    post_excerpt = fun.striphtml(post_excerpt).replace('\n', '').rstrip()
    
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if len(quiz_title) <= 51:
        quiz_title += " - Sosyorol"

    current_user = setup_current_user(current_uid)
    new_quiz = Post(post_title=quiz_title, post_content=quiz_desc, post_date=dt.datetime.now(), author=current_user, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="poll", post_excerpt=post_excerpt, post_parent=0)
    new_quiz.save()
    new_quiz = Post.objects.filter(post_title=quiz_title).order_by('-post_date')[0]

    for (k, v) in communities.items():
        term = Community.objects.filter(name=str(v))[0]
        term_tax = TermTaxonomy.objects.get(term=term)
        new_relation = TermRelationship(object_id=new_quiz.ID, term_taxonomy_id=term_tax.term_taxonomy_id, term_order=0)
        new_relation.save()

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

    response_data = {}
    response_data['content'] = "success"                   
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savecomment(request):
    current_uid = 8
    current_user = setup_current_user(current_uid)
    comment = request.POST["comment"]
    post_id = request.POST["post_id"]
    parent_id = request.POST["parent_id"]
    new_comment = Comment(comment_approved=1, comment_author=current_user.display_name, comment_content=comment, comment_post_ID=post_id, comment_parent=parent_id, comment_author_email=current_user.user_email, comment_date=dt.datetime.now(), user_id=current_uid)
    new_comment.save()
    response_data = {}
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    response_data['content'] = Languages.objects.filter(lang_code=lang, var_name="comment-saved-successfully")[0].translation
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def savenewanswer(request):
    current_uid = 8
    answer = request.POST["answer"]
    parent_id = int(request.POST["parent"])
    parent = Post.objects.filter(ID=parent_id)[0]
    current_user = setup_current_user(current_uid)
    new_answer = Post(post_title=parent.post_title, post_content=answer, post_date=dt.datetime.now(), author=current_user, post_author=current_uid, to_ping="", pinged="", post_content_filtered="", post_status="publish", post_type="answer", post_excerpt=parent.post_excerpt, post_parent=parent_id)
    new_answer.save()
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    response_data = {}
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
        current_uid = 8
        lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
        word_list = Languages.objects.filter(Q(lang_code = lang))
    except:
        return HttpResponse(json.dumps({}),content_type="application/json")
    return render(request, 'posts/postdetails/quiz_result.html', {'result':result_obj, 'quiz_title':quiz_title, 'word_list':word_list})

def emloymentcredential(request):
    try:
        current_uid = 8
        cred = UserMeta(user_id=current_uid, meta_key="employments", meta_value=json.dumps(request.GET))
        cred.save()
        return "success"
    except:
        return "error"

def educationcredential(request):
    try:
        current_uid = 8
        cred = UserMeta(user_id=current_uid, meta_key="educations", meta_value=json.dumps(request.GET))
        cred.save()
        return "success"
    except:
        return "error"

def locationcredential(request):
    try:
        current_uid = 8
        cred = UserMeta(user_id=current_uid, meta_key="locations", meta_value=json.dumps(request.GET))
        cred.save()
        return "success"
    except:
        return "error"

def languagecredential(request):
    try:
        current_uid = 8
        cred = UserMeta(user_id=current_uid, meta_key="languages", meta_value=json.dumps(request.GET))
        cred.save()
        return "success"
    except:
        return "error"

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
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({}), content_type="application/json")

'''---------------------------------------
  VIEWS              
-----------------------------------------'''
def opensosyorol(request):
    try:
        uid = request.session["uid"]
        if uid is not None:
            user = auth.get_user(uid)
            print('Successfully fetched user data: {0}'.format(user.uid))
            return home(request)
    except:
        try:
            uid = request.POST.get("uid")
            if uid is not None:
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
    '''
    try:
        redirect = request.POST.get("uid")
    except:
        redirect = "/"
    '''
    redirect = "/"
    request.session["uid"] = None
    return HttpResponseRedirect(redirect)

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
    start_start = time.time()
    current_uid = 8

    start = time.time()
    current_user = setup_current_user(current_uid)
    end = time.time() - start
    print(f"User setup in {end} s")

    start = time.time()
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    end = time.time() - start
    print(f"Preference setup in {end} s")

    start = time.time()
    word_list = Languages.objects.filter(Q(lang_code = lang))
    end = time.time() - start
    print(f"Get word list in {end} s")

    
    start = time.time()
    header_dict = header(word_list)
    end = time.time() - start
    print(f"Set header_dict in {end} s")

    start = time.time()
    feed_dict = feed(word_list)
    end = time.time() - start
    print(f"Set feed_dict in {end} s")

    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.get(var_name = 'select-language').translation)
    
    myprofile = fun.ucfirst(word_list.get(var_name = 'my-profile').translation)
    createpost = fun.ucfirst(word_list.get(var_name = 'create-post').translation)
    seeall = fun.ucfirst(word_list.get(var_name = 'see-all').translation)
    populercommunities = fun.ucfirst(word_list.get(var_name = 'popular-communities').translation)
    subscribe = fun.ucfirst(word_list.get(var_name = 'subscribe').translation)

    start = time.time()
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    end = time.time() - start
    print(f"Get followed communities in {end} s")

    start = time.time()
    popular_communities = TermTaxonomy.objects.filter(Q(taxonomy="post_tag")).order_by('-count')[:5].prefetch_related()
    end = time.time() - start
    print(f"Get popular communities in {end} s")

    post_template_dict = post_template(word_list)

    start = time.time()
    posts = Post.objects.filter(post_type="post", post_status="publish").order_by('-post_date')[1055:1056].prefetch_related()
    for post in posts:
        setup_postmeta(post, word_list)
    end = time.time() - start
    print(f"Get and setup posts in {end} s")

    start = time.time()
    links = Post.objects.filter(post_type="link", post_status="publish").order_by('-post_date')[:1].prefetch_related()
    for post in links:
        setup_postmeta(post, word_list)
        post.photo_from_url = fun.get_photo_from_url(post.post_content)
    end = time.time() - start
    print(f"Get and setup links in {end} s")

    start = time.time()
    answers = Post.objects.filter(post_type="answer", post_status="publish").order_by('-post_date')[:1].prefetch_related()
    for post in answers:
        setup_postmeta(post, word_list)
    end = time.time() - start
    print(f"Get and setup answers in {end} s")

    start = time.time()
    questions = Post.objects.filter(post_type="questions", post_status="publish").order_by('-post_date')[:8]
    for question in questions:
        setup_postmeta(question, word_list)
    end = time.time() - start
    print(f"Get and setup questions in {end} s")

    start = time.time()
    polls = Post.objects.filter(post_type="poll", post_status="publish").order_by('-post_date')[:1].prefetch_related()
    for poll in polls:
        setup_postmeta(poll, word_list)
    end = time.time() - start
    print(f"Get and setup polls in {end} s")

    start = time.time()
    mediaposts = Post.objects.filter(post_type="media", post_status="publish").order_by('-post_date').prefetch_related()
    for m in mediaposts:
        setup_postmeta(m, word_list)
        setup_mediameta(m)
    end = time.time() - start
    print(f"Get and setup media in {end} s")

    start = time.time()
    """community = Community.objects.filter(slug="test")[0]
    taxonomy = TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
    post_ids = TermRelationship.objects.filter(Q(term_taxonomy_id=taxonomy))
    post_ids = list({x.object_id: x for x in post_ids}.keys())"""
    post_ids = PostMeta.objects.filter(meta_key="quiz_type", meta_value="text")
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    quizzes = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')[:4].prefetch_related()
    for quiz in quizzes:
        print(quiz.ID)
        setup_postmeta(quiz, word_list)
        setup_quizmeta(quiz, word_list)
    end = time.time() - start
    print(f"Get and setup quizzes in {end} s")

    start = time.time()
    post_ids = PostMeta.objects.filter(meta_key="quiz_type", meta_value="colorBox")
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    colorBox_quizzes = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')[:4].prefetch_related()
    for quiz in colorBox_quizzes:
        quiz.post_title = quiz.post_title.replace(" - Sosyorol", "")
        setup_postmeta(quiz, word_list)
        setup_colorbox_quizmeta(quiz, word_list)
    end = time.time() - start
    print(f"Get and setup colorbox quizzes in {end} s")

    start = time.time()
    post_ids = PostMeta.objects.filter(meta_key="quiz_type", meta_value="media")
    post_ids = list({x.post_id: x for x in post_ids}.keys())
    media_quizzes = Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')[:4].prefetch_related()
    for quiz in media_quizzes:
        quiz.post_title = quiz.post_title.replace(" - Sosyorol", "")
        setup_postmeta(quiz, word_list)
        setup_media_quizmeta(quiz, word_list)
    end = time.time() - start
    print(f"Get and setup media quizzes in {end} s")

    start = time.time()
    communities = Community.objects.all()[:10]
    end = time.time() - start
    print(f"Get communities in {end} s")

    start = time.time()
    user_queryset = User.objects.all()[:10]
    users = []
    for user in user_queryset:
        user = setup_current_user(user.ID)
        users.append(user)
    end = time.time() - start
    print(f"Get users in {end} s")

    start = time.time()
    comment_editor = comment_editor_dict(word_list)
    end = time.time() - start
    print(f"Setup comment editor in {end} s")

    end_end = time.time() - start_start
    print(f"Total: {end_end} s")
    return render(request, 'index.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities, 'feed_dict':feed_dict,
                                            'popular_communities':popular_communities, 'posts':posts,
                                            'post_template_dict':post_template_dict, 'comment_editor':comment_editor,
                                            'links':links, 'answers':answers, 'questions':questions, 'quizzes':quizzes,
                                            'communities':communities, 'users':users, 'polls':polls,
                                            'word_list':word_list, 'colorBox_quizzes':colorBox_quizzes, 'media_quizzes':media_quizzes, 'mediaposts':mediaposts
                                            })

def search(request, **kwargs):
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    search_key = ""
    try:
        search_key = request.POST["search_key"]
        print(search_key)
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
        for question in question_results:
            setup_postmeta(question, word_list)
    
    user_results = {}
    if fltr == "profile" or fltr == "all":
        user_results = User.objects.filter(Q(display_name__icontains=search_key))
        for user in user_results:
            user_desc = UserMeta.objects.filter(Q(user_id = user.ID)).filter(Q(meta_key = 'description'))[0]
            user.set_description(user_desc.meta_value)
            mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{user.ID}')
            if (os.path.exists(mypath)):
                onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(user.ID) + "/" + onlyfiles[0]
            else:
                avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
            user.set_avatar(avatar_url)

    #Right
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
    return render(request, "search.html", {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'country_list':country_list,
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
    current_uid = 8

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
    header_dict = header(word_list)
    current_user = setup_current_user(current_uid)
    page_dict = history_dict(word_list)

    left_menu_dict = left_menu(word_list)
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = fun.ucfirst(c.translation)

    post_types_dict = post_types(word_list)
    search_history = SearchHistory.objects.filter(Q(user_id=current_uid)).filter(Q(is_deleted=0)).filter(Q(search_term__icontains=query))
    post_history = PostHistory.objects.filter(Q(user_id=current_uid)).filter(Q(is_deleted=0))
    comment_editor = comment_editor_dict(word_list)
    post_template_dict = post_template(word_list)
    for p in post_history:
        if fltr == "all" or fltr == p.post.post_type:
            setup_postmeta(p.post, word_list)
            if p.post.post_type == "link":
                post.photo_from_url = fun.get_photo_from_url(post.post_content)

    community_history = CommunityHistory.objects.filter(Q(user_id=current_uid)).filter(Q(is_deleted=0))
    for c in community_history:
        follower_ids = FollowedCommunities.objects.filter(Q(term=c.term))
        follower_ids = list({x.user_id: x for x in follower_ids}.keys())
        c.term.followers = User.objects.filter(Q(ID__in=follower_ids))
            
    user_history = UserHistory.objects.filter(Q(user_id=current_uid)).filter(Q(is_deleted=0))
    for user in user_history:
        user_desc = UserMeta.objects.filter(Q(user_id = user.visited_user.ID)).filter(Q(meta_key = 'description'))[0]
        user.visited_user.set_description(user_desc.meta_value)
        mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{user.visited_user.ID}')
        if (os.path.exists(mypath)):
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(user.visited_user.ID) + "/" + onlyfiles[0]
        else:
            avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        user.visited_user.set_avatar(avatar_url)
    
    history = sorted(chain(search_history, post_history, community_history, user_history), key=lambda instance: instance.date, reverse=True)
    history_groups = {}
    for h in history:
        dict_key = h.date
        locale.setlocale(locale.LC_TIME, lang.replace("-","_"))
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
                    

    print(history_groups)

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
    return render(request, "history.html", {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'right_menu_dict':right_menu_dict, 'users':users, 'post_types_dict':post_types_dict,
                                            'page_dict':page_dict, 'filter':fltr, 'history':history_groups,
                                            'comment_editor':comment_editor, 'post_template_dict':post_template_dict, 'query':query,
                                            'word_list':word_list})

@csrf_exempt
def lists(request):
    print("lists")
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
                                            'listsyoumaylike':listsyoumaylike, 'followedlists':followedlists, 'limit':limit,
                                            'word_list':word_list
                                            })

def newpost(request):
    print("new post")
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
                                            'newpost_actions_dict':newpost_actions_dict, 'drafts':drafts, 'word_list':word_list})

def createlist(request):
    print("hello create list")
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
                                            'tips':tips, 'create_list_dict':create_list_dict,'word_list':word_list})

def listdetail(request, slug, **kwargs):
    print("list detail")
    if slug == "undefined" or slug == "create":
        return createlist(request)
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"

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
                                            'filter':fltr,'word_list':word_list}))

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
                                            'filter':fltr, 'word_list':word_list}))

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
                                            'right_menu_dict':right_menu_dict, 'users':users, 'word_list':word_list
                                            })

def savedpostsfilter(request, post_type):
    return savedposts(request, filter=post_type)

def communities(request, **kwargs):
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
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    select_language = fun.ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    categories = CommunityCategories.objects.all()
    random_cat1 = categories.order_by('?')[0]
    random_cat2 = categories.order_by('?')[1]
    if fltr == "all":
        communities = Community.objects.all()[0:20]
    else:
        selected_category = CommunityCategories.objects.get(name=fun.localized_upper(fltr))
        communities = CommunityCategoryRelation.objects.filter(category=selected_category)[:20]
    random_communities1 = CommunityCategoryRelation.objects.filter(category=random_cat1)[:5]
    random_communities2 = CommunityCategoryRelation.objects.filter(category=random_cat2)[:5]
    return render(request, 'communities/communities.html', {'current_user':current_user, 'lang':lang, 'dark':dark,
                                                            'word_list':word_list, 'header_dict':header_dict,
                                                            'country_list':country_list, 'select_language':select_language,
                                                            'categories':categories, 'communities':communities, 
                                                            'random_cat1':random_cat1, 'random_cat2':random_cat2,
                                                            'random_communities1':random_communities1, 'random_communities2':random_communities2, 'filter':fltr})

def communitydetail(request, slug,  **kwargs):
    print("community detail")
    if slug == "lists":
        path = kwargs.get("filter")
        tokens = path.split("/")
        if (len(tokens) == 1):
            print(kwargs)
            print(path)
            return listdetail(request, path)
        else:
            return listdetailfilter(request, tokens[0], post_type=tokens[1])
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

    #Save history
    history = CommunityHistory.objects.filter(Q(user_id=current_uid)).filter(Q(term=community)).filter(Q(is_deleted=0))
    if len(history) > 0:
        counter = history[0].counter + 1
        history.update(date=dt.datetime.now(), counter=counter)
    else:
        history = CommunityHistory(user_id=current_uid, term=community, date=dt.datetime.now(), is_deleted=0, counter=1)
        history.save()

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
                                                                'moderators':moderators, 'current_user': current_user, 'word_list':word_list
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
                                            'new_community_tips_dict':new_community_tips_dict, 'word_list':word_list})

def postdetail(request, username, post_id, slug):
    pid = int(post_id.replace("s", "x"), 16) - 100000
    post = Post.objects.filter(ID=pid)[0]
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    setup_postmeta(post, word_list)
    if post.post_type == "media":
        setup_mediameta(post)
    elif post.post_type == "poll":
        setup_pollmeta(post, word_list)
    elif post.post_type == "link":
        post.photo_from_url = fun.get_photo_from_url(post.post_content)
    elif post.post_type == "questions":
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
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    post.flairs = PostFlair.objects.filter(post=post)
    post.comments = Comment.objects.filter(comment_post_ID=post.ID, comment_parent=0).order_by('-comment_date').prefetch_related()
    comment_length = len(post.comments)
    post.comments = post.comments[:5]
    for comment in post.comments:
        comment.user = setup_current_user(comment.user.ID)
        comment.child_comments = Comment.objects.none()
        comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
        getgrandchildcomments(post.ID, comment.child_comments)
    return render(request, 'postdetail.html', {'post':post, 'lang':lang, 'dark':dark, 
                                                'current_user': current_user, 'word_list':word_list,
                                                'followed_communities':followed_communities, 'comments':post.comments, 'comment_length':comment_length
                                                })
    
def answerdetail(request, parent_author_name, parent_post_id, parent_slug, author_name):
    print("answer detail")
    pid = int(parent_post_id.replace("s", "x"), 16) - 100000
    author = User.objects.filter(user_login=author_name)[0]
    post = Post.objects.filter(post_parent=pid, post_author=author.ID, post_type="answer", post_status="publish")[0]
    post.parent = Post.objects.filter(ID=pid)[0]
    post.parent.guid = arrange_post_slug(post.parent.post_title)
    post.parent.hex_id = hex(post.parent.ID + 100000).replace("x", "s")
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date').prefetch_related()
    setup_postmeta(post, word_list)
    post.comments = Comment.objects.filter(comment_post_ID=post.ID, comment_parent=0).order_by('-comment_date').prefetch_related()
    comment_length = len(post.comments)
    post.comments = post.comments[:5]
    for comment in post.comments:
        comment.user = setup_current_user(comment.user.ID)
        comment.child_comments = Comment.objects.none()
        comment.child_comments = getchildcomments(post.ID, comment.comment_ID)
        getgrandchildcomments(post.ID, comment.child_comments)
    return render(request, 'answerdetail.html', {'post':post, 'lang':lang, 'dark':dark, 
                                                'current_user': current_user, 'word_list':word_list,
                                                'followed_communities':followed_communities, 'comments':post.comments, 'comment_length':comment_length
                                                })

def userprofile(request, username,  **kwargs):
    current_uid = 8
    current_user = setup_current_user(current_uid)
    profile = setup_current_user(User.objects.filter(user_login=username)[0].ID)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    if 'filter' in kwargs:
        fltr = kwargs.get("filter")
    else:
        fltr = "all"
    if fltr == "post":
        profile.posts = profile.posts.filter(Q(post_type="post"))
    elif fltr == "link":
        profile.posts = profile.posts.filter(Q(post_type="link"))
    elif fltr == "poll":
        profile.posts = profile.posts.filter(Q(post_type="poll"))
    elif fltr == "quiz":
        profile.posts = profile.posts.filter(Q(post_type="quiz"))
    elif fltr == "answer":
        profile.posts = profile.posts.filter(Q(post_type="answer"))
    elif fltr == "question":
        profile.posts = profile.posts.filter(Q(post_type="question"))
    elif fltr == "media":
        profile.posts = profile.posts.filter(Q(post_type="media"))
    index = 0
    for post in profile.posts:
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
        index += 1
    profile.posts = profile.posts[:5]
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    employments = UserMeta.objects.filter(user_id = current_uid, meta_key = 'employments').order_by('-umeta_id')
    if employments.count() > 0:
        current_employment = json.loads(employments[0].meta_value)
        position = current_employment["position"]
        company = current_employment["company"]
        profile.employments = word_list.filter(var_name="employment-string")[0].translation.replace("{position}", position).replace("{company}",company)
    
    educations = UserMeta.objects.filter(user_id = current_uid, meta_key = 'educations').order_by('-umeta_id')
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
    
    locations = UserMeta.objects.filter(user_id = current_uid, meta_key = 'locations').order_by('-umeta_id')
    if locations.count() > 0:
        current_location = json.loads(locations[0].meta_value)
        location = current_location["location"]
        startDate = current_location["startDate"]
        endDate = current_location["endDate"]
        if endDate == "current":
            profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
        else:
            datetime_object = dt.datetime.strptime(graduation, '%Y-%m')
            now = dt.datetime.now()
            if datetime_object > now:
                profile.locations = word_list.filter(var_name="lives-in")[0].translation.replace("{location}", location)
            else:
                profile.locations = word_list.filter(var_name="lived-in")[0].translation.replace("{location}", location) + "<span class='cg fwlight'> " +startDate[0:4]+ "-" + endDate[0:4] + "</span>"
    
    languages = UserMeta.objects.filter(user_id = current_uid, meta_key = 'languages').order_by('-umeta_id')
    if languages.count() > 0:
        current_language = json.loads(languages[0].meta_value)
        language = current_language["language"]
        language_id = Languages.objects.filter(var_name__icontains="lang-ns-", translation=language)[0].var_name
        language = Languages.objects.filter(var_name=language_id, lang_code=lang)[0].translation
        profile.languages = word_list.filter(var_name="knows-lang-string")[0].translation.replace("{language}", language)
    
    photos = PostMeta.objects.filter(meta_key="media_type", meta_value="image")
    photos = list({x.post_id: x for x in photos}.keys())
    medias = Post.objects.filter(ID__in=photos, post_author=profile.ID, post_status="publish", post_type="media").order_by('-post_date')[:6]
    for media in medias:
        setup_postmeta(media, word_list)
        setup_mediameta(media)
    return render(request, 'profile.html', {'current_user':current_user, 'lang':lang, 'dark':dark, 'word_list':word_list, 
                                            'profile':profile, 'filter':fltr, 'country_list':country_list, 'medias':medias
                                            })

def settings(request):
    current_uid = 8
    current_user = setup_current_user(current_uid)
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'language').meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).get(meta_key = 'mode').meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    return render(request, 'profilesettings.html', {'current_user':current_user, 'lang':lang, 'dark':dark, 'word_list':word_list})


