from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from sosyorol.models import *
from sosyorol.forms import *
import mysql.connector
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
from io import BytesIO
import sosyorol.functions as fun
import locale

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def humanizedate(date, word_list, to=None):
    sec_text = localized_lower(word_list.filter(Q(var_name = 'sec'))[0].translation)
    secs_text = localized_lower(word_list.filter(Q(var_name = 'secs'))[0].translation)
    min_text = localized_lower(word_list.filter(Q(var_name = 'min'))[0].translation)
    mins_text = localized_lower(word_list.filter(Q(var_name = 'mins'))[0].translation)
    hour_text = localized_lower(word_list.filter(Q(var_name = 'hour'))[0].translation)
    hours_text = localized_lower(word_list.filter(Q(var_name = 'hours'))[0].translation)
    day_text = localized_lower(word_list.filter(Q(var_name = 'day'))[0].translation)
    days_text = localized_lower(word_list.filter(Q(var_name = 'days'))[0].translation)
    week_text = localized_lower(word_list.filter(Q(var_name = 'week'))[0].translation)
    weeks_text = localized_lower(word_list.filter(Q(var_name = 'weeks'))[0].translation)
    month_text = localized_lower(word_list.filter(Q(var_name = 'month'))[0].translation)
    months_text = localized_lower(word_list.filter(Q(var_name = 'months'))[0].translation)
    year_text = localized_lower(word_list.filter(Q(var_name = 'year'))[0].translation)
    years_text = localized_lower(word_list.filter(Q(var_name = 'years'))[0].translation)
    ago = localized_lower(word_list.filter(Q(var_name = 'ago'))[0].translation)
    if to is None:
        to = dt.datetime.now()
    diff = to - date
    seconds = diff.total_seconds()
    if seconds < 3600:
        if seconds < 60:
            if seconds == 1:
                return f"{int(seconds)} {sec_text} {ago}"
            else:
                if seconds <= 0:
                    return f"1 {sec_text} {ago}"
                return f"{int(seconds)} {secs_text} {ago}"
        else:
            mins = int(seconds/60)
            if mins == 1:
                return f"{mins} {min_text} {ago}"
            else:
                return f"{mins} {mins_text} {ago}"
    elif seconds >= 3600 and seconds < (3600*24):
        hours = int(seconds/3600)
        if hours == 1:
            return f"{hours} {hour_text} {ago}"
        else:
            return f"{hours} {hours_text} {ago}"
    elif seconds >= (3600*24) and seconds < (3600*24*7):
        days = int(seconds/(3600*24))
        if days == 1:
            return f"{days} {day_text} {ago}"
        else:
            return f"{days} {days_text} {ago}"
    elif seconds >=  (3600*24*7) and seconds < (3600*24*30):
        weeks = int(seconds/(3600*24*7))
        if weeks == 1:
            return f"{weeks} {week_text} {ago}"
        else:
            return f"{weeks} {weeks_text} {ago}"
    elif seconds >= (3600*24*30) and seconds < (3600*24*365 + 3600*6):
        months = int(seconds/(3600*24*30))
        if months == 1:
            return f"{months} {month_text} {ago}"
        else:
            return f"{months} {months_text} {ago}"
    else:
        years = int(seconds/(3600*24*365 + 3600*6))
        if years == 1:
            return f"{years} {year_text} {ago}"
        else:
            return f"{years} {years_text} {ago}"

def localized_lower(txt):
    rep = [ ('İ','i'), ('I','ı'), ('Ğ','ğ'),('Ü','ü'), ('Ş','ş'), ('Ö','ö'),('Ç','ç')]
    for search, replace in rep:
        txt = txt.replace(search, replace)
    return txt.lower()

def localized_upper(txt):
    rep = [ ('İ','i'), ('I','ı'), ('Ğ','ğ'),('Ü','ü'), ('Ş','ş'), ('Ö','ö'),('Ç','ç')]
    for search, replace in rep:
        txt = txt.replace(replace, search)
    return txt.upper()

def ucfirst(txt):
    txt = localized_lower(txt)
    return localized_upper(txt[0]) + txt[1:]

def ucwords(txt):
    txt = localized_lower(txt)
    words = txt.split()
    for i in range(0, len(words)):
        words[i] = ucfirst(words[i])
    return " ".join(words)

def header(word_list):
    header_dict = {}
    home = word_list.filter(Q(var_name = 'home'))[0].translation.upper()
    quizzes = word_list.filter(Q(var_name = 'quizzes'))[0].translation.upper()
    questions = word_list.filter(Q(var_name = 'questions'))[0].translation.upper()
    polls = word_list.filter(Q(var_name = 'polls'))[0].translation.upper()
    communities = word_list.filter(Q(var_name = 'communities'))[0].translation.upper()
    settings = ucfirst(word_list.filter(Q(var_name = 'settings'))[0].translation)
    profile = ucfirst(word_list.filter(Q(var_name = 'profile'))[0].translation)
    messages = ucfirst(word_list.filter(Q(var_name = 'messages'))[0].translation)
    search = ucfirst(word_list.filter(Q(var_name = 'search'))[0].translation)
    notifications = ucfirst(word_list.filter(Q(var_name = 'notifications'))[0].translation)
    header_dict['createpost'] = ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
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
    left_menu_dict['createpost'] = ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    left_menu_dict['feed'] = ucfirst(word_list.filter(Q(var_name = 'feed'))[0].translation)
    left_menu_dict['darkmode'] = ucfirst(word_list.filter(Q(var_name = 'dark-mode'))[0].translation)
    left_menu_dict['lightmode'] = ucfirst(word_list.filter(Q(var_name = 'light-mode'))[0].translation)
    left_menu_dict['country'] = ucfirst(word_list.filter(Q(var_name = 'lang'))[0].translation)
    left_menu_dict['about'] = ucfirst(word_list.filter(Q(var_name = 'about'))[0].translation)
    left_menu_dict['careers'] = ucfirst(word_list.filter(Q(var_name = 'careers'))[0].translation)
    left_menu_dict['advertise'] = ucfirst(word_list.filter(Q(var_name = 'advertise'))[0].translation)
    left_menu_dict['helpvar'] = ucfirst(word_list.filter(Q(var_name = 'help'))[0].translation)
    left_menu_dict['termsvar'] = ucfirst(word_list.filter(Q(var_name = 'terms'))[0].translation)
    left_menu_dict['createlist'] = ucwords(word_list.filter(Q(var_name = 'create-list'))[0].translation)
    left_menu_dict['lists'] = ucfirst(word_list.filter(Q(var_name = 'lists'))[0].translation)
    left_menu_dict['visithistory'] = ucfirst(word_list.filter(Q(var_name = 'visithistory'))[0].translation)
    left_menu_dict['savedposts'] = ucfirst(word_list.filter(Q(var_name = 'savedposts'))[0].translation)
    left_menu_dict['more'] = ucfirst(word_list.filter(Q(var_name = 'more'))[0].translation)
    left_menu_dict['less'] = ucfirst(word_list.filter(Q(var_name = 'less'))[0].translation)
    return left_menu_dict

def lists_achive(word_list):
    lists_dict = {}
    lists_dict['lists'] = ucfirst(word_list.filter(Q(var_name = 'lists'))[0].translation)
    lists_dict['listsPageDesc'] = ucfirst(word_list.filter(Q(var_name = 'lists_page_desc'))[0].translation)
    lists_dict['createList'] = ucwords(word_list.filter(Q(var_name = 'create-list'))[0].translation)
    lists_dict['followLists'] = ucwords(word_list.filter(Q(var_name = 'follow-lists'))[0].translation)
    lists_dict['yourlists'] = ucwords(word_list.filter(Q(var_name = 'your-lists'))[0].translation)
    lists_dict['all'] = ucfirst(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    lists_dict['createdbyyou'] = ucfirst(word_list.filter(Q(var_name = 'created-by-you'))[0].translation)
    lists_dict['addlist'] = ucwords(word_list.filter(Q(var_name = 'add-list'))[0].translation)
    lists_dict['listsyoumaylike'] = ucwords(word_list.filter(Q(var_name = 'lists-you-may-like'))[0].translation)
    lists_dict['listsyoumaylikeinfo'] = ucfirst(word_list.filter(Q(var_name = 'lists-you-may-like-info'))[0].translation)
    lists_dict['featured'] = ucwords(word_list.filter(Q(var_name = 'featured'))[0].translation)
    lists_dict['post'] = ucfirst(word_list.filter(Q(var_name = 'post'))[0].translation)
    lists_dict['members'] = ucfirst(word_list.filter(Q(var_name = 'members'))[0].translation)
    lists_dict['followers'] = ucfirst(word_list.filter(Q(var_name = 'followers'))[0].translation)
    lists_dict['follow'] = ucfirst(word_list.filter(Q(var_name = 'follow'))[0].translation)
    lists_dict['following'] = ucwords(word_list.filter(Q(var_name = 'following'))[0].translation)
    lists_dict['editlist'] = ucwords(word_list.filter(Q(var_name = 'edit-list'))[0].translation)
    return lists_dict

def list_info(word_list):
    list_info_dict = {}
    list_info_dict["aboutlist"] = ucwords(word_list.filter(Q(var_name = 'about-list'))[0].translation)
    list_info_dict["datecreated"] = ucwords(word_list.filter(Q(var_name = 'date-created'))[0].translation)
    list_info_dict["createdby"] = ucwords(word_list.filter(Q(var_name = 'created_by'))[0].translation)
    return list_info_dict

def right_menu(word_list):
    right_menu_dict = {}
    right_menu_dict['interaction'] = ucwords(word_list.filter(Q(var_name = 'interaction'))[0].translation)
    right_menu_dict['scrolltotop'] = localized_upper(word_list.filter(Q(var_name = 'scroll-to-top'))[0].translation)
    right_menu_dict['viewprofile'] = ucwords(word_list.filter(Q(var_name = 'go-to-profile'))[0].translation)
    right_menu_dict['myprofile'] = ucwords(word_list.filter(Q(var_name = 'my-profile'))[0].translation)
    right_menu_dict['createpost'] = ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    right_menu_dict['seeall'] = ucwords(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    right_menu_dict['popularcommunities'] = ucwords(word_list.filter(Q(var_name = 'popular-communities'))[0].translation)
    right_menu_dict['subscribe'] = ucwords(word_list.filter(Q(var_name = 'subscribe'))[0].translation)
    right_menu_dict['trendsofcountrytitle'] = ucfirst(word_list.filter(Q(var_name = 'trends-of-country-title'))[0].translation)
    right_menu_dict['showmore'] = ucfirst(word_list.filter(Q(var_name = 'show-more'))[0].translation)
    right_menu_dict['usersyoumayfollow'] = ucfirst(word_list.filter(Q(var_name = 'users-you-may-follow'))[0].translation)
    right_menu_dict['follow'] = ucfirst(word_list.filter(Q(var_name = 'follow'))[0].translation)
    return right_menu_dict

def feed(word_list):
    feed_dict = {}
    feed_dict['createpost'] = ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    feed_dict['trend'] = ucwords(word_list.filter(Q(var_name = 'trends'))[0].translation)
    feed_dict['new'] = ucwords(word_list.filter(Q(var_name = 'new'))[0].translation)
    feed_dict['contra'] = ucwords(word_list.filter(Q(var_name = 'controversial'))[0].translation)
    feed_dict['rising'] = ucwords(word_list.filter(Q(var_name = 'rising'))[0].translation)
    feed_dict['best'] = ucwords(word_list.filter(Q(var_name = 'best'))[0].translation)
    feed_dict['now'] = ucwords(word_list.filter(Q(var_name = 'now'))[0].translation)
    feed_dict['today'] = ucwords(word_list.filter(Q(var_name = 'today'))[0].translation)
    feed_dict['thisweek'] = ucwords(word_list.filter(Q(var_name = 'this-week'))[0].translation)
    feed_dict['thismonth'] = ucwords(word_list.filter(Q(var_name = 'this-month'))[0].translation)
    feed_dict['thisyear'] = ucwords(word_list.filter(Q(var_name = 'this-year'))[0].translation)
    feed_dict['alltime'] = ucwords(word_list.filter(Q(var_name = 'all-time'))[0].translation)
    feed_dict['answerthequestions'] = ucwords(word_list.filter(Q(var_name = 'all-time'))[0].translation)
    feed_dict['discovernewtopics'] = ucwords(word_list.filter(Q(var_name = 'discover-more-communities'))[0].translation)
    feed_dict['morem'] = ucwords(word_list.filter(Q(var_name = 'more'))[0].translation)
    feed_dict['followmoreusers'] = ucwords(word_list.filter(Q(var_name = 'follow-more-users'))[0].translation)
    feed_dict['hiddentakeback'] = ucwords(word_list.filter(Q(var_name = 'hidden-take-back'))[0].translation)
    feed_dict['hiddenusers'] = ucwords(word_list.filter(Q(var_name = 'hidden-users'))[0].translation)
    feed_dict['media'] = ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    feed_dict['link'] = ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    feed_dict['quiz'] = ucwords(word_list.filter(Q(var_name = 'quiz'))[0].translation)
    feed_dict['poll'] = ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    feed_dict['question'] = ucwords(word_list.filter(Q(var_name = 'question'))[0].translation)
    feed_dict['answerthequestions'] = ucwords(word_list.filter(Q(var_name = 'answer-the-questions'))[0].translation)
    feed_dict['discoverthenewtopics'] = ucwords(word_list.filter(Q(var_name = 'discover-more-communities'))[0].translation)
    feed_dict['followmoreusers'] = ucwords(word_list.filter(Q(var_name = 'follow-more-users'))[0].translation)
    feed_dict['follow'] = ucwords(word_list.filter(Q(var_name = 'follow'))[0].translation)
    return feed_dict

def post_template(word_list):
    post_template_dict = {}
    post_template_dict['article'] = ucwords(word_list.filter(Q(var_name = 'article'))[0].translation)
    post_template_dict['media'] = ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    post_template_dict['link'] = ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    post_template_dict['answer'] = ucwords(word_list.filter(Q(var_name = 'answer'))[0].translation)
    post_template_dict['poll'] = ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    post_template_dict['answernoun'] = ucwords(word_list.filter(Q(var_name = 'answer-noun'))[0].translation)
    post_template_dict['recommendedfy'] = ucwords(word_list.filter(Q(var_name = 'recommended-for-you'))[0].translation)
    post_template_dict['more'] = ucwords(word_list.filter(Q(var_name = 'more'))[0].translation)
    post_template_dict['share'] = ucwords(word_list.filter(Q(var_name = 'share'))[0].translation)
    post_template_dict['comments'] = ucwords(word_list.filter(Q(var_name = 'comments'))[0].translation)
    post_template_dict['repost'] = ucwords(word_list.filter(Q(var_name = 'repost'))[0].translation)
    post_template_dict['upvote'] = ucwords(word_list.filter(Q(var_name = 'upvote'))[0].translation)
    post_template_dict['downvote'] = ucwords(word_list.filter(Q(var_name = 'downvote'))[0].translation)
    post_template_dict['send'] = ucwords(word_list.filter(Q(var_name = 'send'))[0].translation)
    post_template_dict['subscribe'] = ucwords(word_list.filter(Q(var_name = 'subscribe'))[0].translation)
    post_template_dict['vote'] = ucwords(word_list.filter(Q(var_name = 'vote'))[0].translation)
    post_template_dict['votenoun'] = localized_lower(word_list.filter(Q(var_name = 'vote-noun'))[0].translation)
    post_template_dict['votesnoun'] = localized_lower(word_list.filter(Q(var_name = 'votes-noun'))[0].translation)
    return post_template_dict

def comment_editor_dict(word_list):
    comment_editor = {}
    comment_editor['addcomment'] = ucfirst(word_list.filter(Q(var_name = 'add-comment'))[0].translation)
    comment_editor['send'] = ucwords(word_list.filter(Q(var_name = 'send'))[0].translation)
    return comment_editor

def get_photo_from_url(photo_url):
    webpage = urlopen(photo_url).read()
    link = BSHTML(webpage, "html.parser")
    """Attempt to get a preview image."""
    image = ''
    if link.find("meta", property="og:image") is not None:
        image = link.find("meta", property="og:image").get('content')
    elif link.find("img") is not None:
        image = link.find("img").get('href')
    return image

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
        post.poll_duration_left = ucwords(word_list.filter(Q(var_name = 'unlimited-time'))[0].translation)
    else:
        days = int(duration.split()[0])
        ago = localized_lower(word_list.filter(Q(var_name = 'ago'))[0].translation)
        left = localized_lower(word_list.filter(Q(var_name = 'left'))[0].translation)
        to = post.post_date.replace(tzinfo=None) + dt.timedelta(days=days)
        now = dt.datetime.now()
        if now < to:
            post.poll_duration_left = humanizedate(now, word_list, to=to).replace(ago, left)
        else:
            post.poll_duration_left = "bitti"       

def setup_postmeta(post, word_list):
    current_uid = 8
    post.like = len(PostRating.objects.filter(Q(post_id=post.ID)).filter(Q(opinion='like')))
    post.dislike = len(PostRating.objects.filter(Q(post_id=post.ID)).filter(Q(opinion='dislike')))
    post.rating = post.like - post.dislike
    post.repost = len(Repost.objects.filter(Q(post_id=post.ID)))
    post.author = User.objects.filter(Q(ID=post.post_author))[0]
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{post.post_author}')
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(post.post_author) + "/" + onlyfiles[0]
    post.author.set_avatar(avatar_url)
    post.time_diff = humanizedate(post.post_date.replace(tzinfo=None), word_list)
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
    short_content = striphtml(short_content).replace('\n', '').rstrip()
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

# Create your views here.
def home(request):
    start = time.perf_counter()
    current_uid = 8
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    right_menu_dict = right_menu(word_list)
    feed_dict = feed(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = ucfirst(c.translation)
    select_language = ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    
    myprofile = ucfirst(word_list.filter(Q(var_name = 'my-profile'))[0].translation)
    createpost = ucfirst(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    seeall = ucfirst(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    populercommunities = ucfirst(word_list.filter(Q(var_name = 'popular-communities'))[0].translation)
    subscribe = ucfirst(word_list.filter(Q(var_name = 'subscribe'))[0].translation)

    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date')
    followed_community_ids = list({x.term_id: x for x in followed_communities}.keys())
    followed_communities = Community.objects.filter(term_id__in=followed_community_ids)
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

    popular_communities = TermTaxonomy.objects.filter(Q(taxonomy="post_tag")).order_by('-count')[:5]
    popular_community_ids = list({x.term_id: x for x in popular_communities}.keys())
    popular_communities = Community.objects.filter(term_id__in=popular_community_ids)
    for i in popular_communities:
        i.count = TermTaxonomy.objects.filter(Q(term_id=i.term_id))[0].count
        i.name = localized_lower(i.name)
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

    post_template_dict = post_template(word_list)
    posts = Post.objects.filter(Q(post_type="post")).filter(Q(post_status="publish")).order_by('-post_date')[1055:1056]
    for post in posts:
        setup_postmeta(post, word_list)

    links = Post.objects.filter(Q(post_type="link")).filter(Q(post_status="publish")).order_by('-post_date')[:1]
    for post in links:
        setup_postmeta(post, word_list)
        post.photo_from_url = get_photo_from_url(post.post_content)

    answers = Post.objects.filter(Q(post_type="answer")).filter(Q(post_status="publish")).order_by('-post_date')[:2]
    for post in answers:
        setup_postmeta(post, word_list)

    questions = Post.objects.filter(Q(post_type="questions")).filter(Q(post_status="publish")).order_by('-post_date')[:8]
    for post in questions:
        setup_postmeta(post, word_list)
    
    polls = Post.objects.filter(Q(post_type="poll")).filter(Q(post_status="publish")).order_by('-post_date')
    for poll in polls:
        setup_postmeta(poll, word_list)

    communities = Community.objects.all()[:10]
    for i in communities:
        i.name = ucwords(i.name)
        i.lower_name = localized_lower(i.name)
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


    users = User.objects.all()[:10]
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
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = ucfirst(c.translation)
    select_language = ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date')[:5]
    followed_community_ids = list({x.term_id: x for x in followed_communities}.keys())
    followed_communities = Community.objects.filter(term_id__in=followed_community_ids)
    for i in followed_communities:
        i.name = ucwords(i.name)
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

def post_types(word_list):
    post_types_dict = {}
    post_types_dict['post'] = ucwords(word_list.filter(Q(var_name = 'post'))[0].translation)
    post_types_dict['media'] = ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    post_types_dict['link'] = ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    post_types_dict['quiz'] = ucwords(word_list.filter(Q(var_name = 'quiz'))[0].translation)
    post_types_dict['poll'] = ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    post_types_dict['question'] = ucwords(word_list.filter(Q(var_name = 'question'))[0].translation)
    post_types_dict['answer'] = ucwords(word_list.filter(Q(var_name = 'answer-noun'))[0].translation)
    return post_types_dict

def create_post_rules(word_list):
    create_post_rules_dict = {}
    create_post_rules_dict["1"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule1'))[0].translation)
    create_post_rules_dict["2"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule2'))[0].translation)
    create_post_rules_dict["3"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule3'))[0].translation)
    create_post_rules_dict["4"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule4'))[0].translation)
    create_post_rules_dict["5"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule5'))[0].translation)
    create_post_rules_dict["6"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule6'))[0].translation)
    create_post_rules_dict["7"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule7'))[0].translation)
    create_post_rules_dict["8"] = ucfirst(word_list.filter(Q(var_name = 'create-post-rule8'))[0].translation)
    return create_post_rules_dict

def create_poll(word_list):
    create_poll_dict = {}
    create_poll_dict["createpoll"] = ucwords(word_list.filter(Q(var_name = 'create-poll'))[0].translation)
    create_poll_dict["option"] = ucwords(word_list.filter(Q(var_name = 'option'))[0].translation)
    create_poll_dict["pollduration"] = ucwords(word_list.filter(Q(var_name = 'poll-duration'))[0].translation)
    create_poll_dict["unlimitedtime"] = ucwords(word_list.filter(Q(var_name = 'unlimited-time'))[0].translation)
    create_poll_dict["day"] = localized_lower(word_list.filter(Q(var_name = 'day'))[0].translation)
    create_poll_dict["days"] = localized_lower(word_list.filter(Q(var_name = 'days'))[0].translation)
    create_poll_dict["addrule"] = ucfirst(word_list.filter(Q(var_name = 'poll-option-add-rule'))[0].translation)
    create_poll_dict["removerule"] = ucfirst(word_list.filter(Q(var_name = 'poll-option-remove-rule'))[0].translation)
    return create_poll_dict

def newpost_actions(word_list):
    newpost_actions_dict = {}
    newpost_actions_dict["title"] = ucwords(word_list.filter(Q(var_name = 'title'))[0].translation)
    newpost_actions_dict['send'] = ucwords(word_list.filter(Q(var_name = 'send'))[0].translation)
    newpost_actions_dict['cancel'] = ucwords(word_list.filter(Q(var_name = 'cancel'))[0].translation)
    newpost_actions_dict['save'] = ucwords(word_list.filter(Q(var_name = 'save'))[0].translation)
    newpost_actions_dict['clear'] = ucwords(word_list.filter(Q(var_name = 'clear'))[0].translation)
    newpost_actions_dict['drafts'] = ucwords(word_list.filter(Q(var_name = 'drafts'))[0].translation)
    newpost_actions_dict['searchcommunity'] = ucwords(word_list.filter(Q(var_name = 'search-community'))[0].translation)
    newpost_actions_dict['spoiler'] = ucfirst(word_list.filter(Q(var_name = 'spoiler-flair'))[0].translation)
    newpost_actions_dict['nsfw'] = ucfirst(word_list.filter(Q(var_name = 'nsfw-flair'))[0].translation)
    newpost_actions_dict['close'] = ucfirst(word_list.filter(Q(var_name = 'close'))[0].translation)
    newpost_actions_dict['delete'] = ucfirst(word_list.filter(Q(var_name = 'delete'))[0].translation)
    newpost_actions_dict['lastupdated'] = ucfirst(word_list.filter(Q(var_name = 'last-updated'))[0].translation)
    return newpost_actions_dict

def newpost(request):
    try:
        post_type = request.GET['post']
    except:
        post_type = "post"
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
    post_types_dict = post_types(word_list)
    create_post_rules_dict = create_post_rules(word_list)
    tips = ucwords(word_list.filter(Q(var_name = 'tips'))[0].translation)
    create_post_dict = {}
    if(post_type == "poll"):
        create_post_dict = create_poll(word_list)
    newpost_actions_dict = newpost_actions(word_list)
    drafts = Post.objects.filter(Q(post_author=current_uid)).filter(post_status="draft").filter(post_type__in=["post", "questions","poll"]).order_by('post_date')
    for post in drafts:
        setup_postmeta(post, word_list)
    return render(request, 'newpost.html', {'post_type':post_type,'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict, 'post_types_dict':post_types_dict,
                                            'create_post_rules_dict': create_post_rules_dict, 'tips':tips, 'create_post_dict':create_post_dict,
                                            'newpost_actions_dict':newpost_actions_dict, 'drafts':drafts})

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

def createlist(request):
    print("createlist")
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
    tips = ucwords(word_list.filter(Q(var_name = 'tips'))[0].translation)
    create_list_dict = {}
    create_list_dict["public"] = ucwords(word_list.filter(Q(var_name = 'public'))[0].translation)
    create_list_dict["private"] = ucwords(word_list.filter(Q(var_name = 'private'))[0].translation)
    create_list_dict["public_info"] = ucfirst(word_list.filter(Q(var_name = 'public_info'))[0].translation)
    create_list_dict["private_info"] = ucfirst(word_list.filter(Q(var_name = 'private_info'))[0].translation)
    create_list_dict["title"] = ucwords(word_list.filter(Q(var_name = 'title'))[0].translation)
    create_list_dict["title_placeholder"] = ucwords(word_list.filter(Q(var_name = 'list_title_placeholder'))[0].translation)
    create_list_dict["desc_placeholder"] = ucfirst(word_list.filter(Q(var_name = 'list_desc_placeholder'))[0].translation)
    create_list_dict["description"] = ucwords(word_list.filter(Q(var_name = 'description'))[0].translation)
    create_list_dict['cancel'] = ucwords(word_list.filter(Q(var_name = 'cancel'))[0].translation)
    create_list_dict['save'] = ucwords(word_list.filter(Q(var_name = 'save'))[0].translation)
    create_list_dict['clear'] = ucwords(word_list.filter(Q(var_name = 'clear'))[0].translation)
    return render(request, 'lists/newlist.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict, 
                                            'tips':tips, 'create_list_dict':create_list_dict})

def savenewlist(request):
    print("savenewlist")
    photo_url = request.POST["photo_url"]
    filename, file_extension = os.path.splitext(photo_url)
    title = request.POST["title"]
    desc = request.POST["desc"]
    color = request.POST["color"]
    is_public = request.POST["privacy"]
    fun.resize_list_image(photo_url)
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
            post.photo_from_url = get_photo_from_url(post.post_content)

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
            post.photo_from_url = get_photo_from_url(post.post_content)

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

def savedposts(request):
    current_uid = 8
    fltr = "all"
    lang = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'language'))[0].meta_value
    dark = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'mode'))[0].meta_value
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
    country_list = Languages.objects.filter(Q(var_name = 'lang'))
    for c in country_list:
        c.translation = ucfirst(c.translation)
    select_language = ucfirst(word_list.filter(Q(var_name = 'select-language'))[0].translation)
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

    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date')
    followed_community_ids = list({x.term_id: x for x in followed_communities}.keys())
    followed_communities = Community.objects.filter(term_id__in=followed_community_ids)
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
        setup_postmeta(item.post, word_list)
        if item.post.post_type == "link":
            item.post.photo_from_url = get_photo_from_url(item.post.post_content)
        savedposts.append(item.post)
    print(savedposts)
    savedposts_dict = {}
    savedposts_dict["saveditems"] = ucfirst(word_list.filter(Q(var_name = 'saveditems'))[0].translation)
    savedposts_dict["saveditemsDesc"] = ucfirst(word_list.filter(Q(var_name = 'saveditemsDesc'))[0].translation)
    savedposts_dict["all"] = ucfirst(word_list.filter(Q(var_name = 'all'))[0].translation)
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
