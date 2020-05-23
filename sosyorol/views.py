from django.shortcuts import render
from django.http import HttpResponse
from sosyorol.models import *
import mysql.connector
from django.db.models import Q
import os
from os import listdir
from os.path import isfile, join


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')

mydb = mysql.connector.connect(
    host="185.87.252.147",
    user="dmlssyrl",
    passwd="190734fB@vesselam",
    database="unhelvasi_wp864"
)
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
    feed = ucfirst(word_list.filter(Q(var_name = 'feed'))[0].translation)
    darkmode = ucfirst(word_list.filter(Q(var_name = 'dark-mode'))[0].translation)
    lightmode = ucfirst(word_list.filter(Q(var_name = 'light-mode'))[0].translation)
    country = ucfirst(word_list.filter(Q(var_name = 'lang'))[0].translation)
    about = ucfirst(word_list.filter(Q(var_name = 'about'))[0].translation)
    careers = ucfirst(word_list.filter(Q(var_name = 'careers'))[0].translation)
    advertise = ucfirst(word_list.filter(Q(var_name = 'advertise'))[0].translation)
    helpvar = ucfirst(word_list.filter(Q(var_name = 'help'))[0].translation)
    termsvar = ucfirst(word_list.filter(Q(var_name = 'terms'))[0].translation)
    left_menu_dict['feed'] = feed
    left_menu_dict['darkmode'] = darkmode
    left_menu_dict['lightmode'] = lightmode
    left_menu_dict['country'] = country
    left_menu_dict['about'] = about
    left_menu_dict['careers'] = careers
    left_menu_dict['advertise'] = advertise
    left_menu_dict['helpvar'] = helpvar
    left_menu_dict['termsvar'] = termsvar
    return left_menu_dict

def right_menu(word_list):
    right_menu_dict = {}
    interaction = ucwords(word_list.filter(Q(var_name = 'interaction'))[0].translation)
    scrolltotop = localized_upper(word_list.filter(Q(var_name = 'scroll-to-top'))[0].translation)
    viewprofile = ucwords(word_list.filter(Q(var_name = 'go-to-profile'))[0].translation)
    myprofile = ucwords(word_list.filter(Q(var_name = 'my-profile'))[0].translation)
    createpost = ucwords(word_list.filter(Q(var_name = 'create-post'))[0].translation)
    seeall = ucwords(word_list.filter(Q(var_name = 'see-all'))[0].translation)
    popularcommunities = ucwords(word_list.filter(Q(var_name = 'popular-communities'))[0].translation)
    subscribe = ucwords(word_list.filter(Q(var_name = 'subscribe'))[0].translation)
    right_menu_dict['interaction'] = interaction
    right_menu_dict['scrolltotop'] = scrolltotop
    right_menu_dict['viewprofile'] = viewprofile
    right_menu_dict['myprofile'] = myprofile
    right_menu_dict['createpost'] = createpost
    right_menu_dict['seeall'] = seeall
    right_menu_dict['popularcommunities'] = popularcommunities
    right_menu_dict['subscribe'] = subscribe
    return right_menu_dict


def feed(word_list):
    feed_dict = {}
    trend = ucwords(word_list.filter(Q(var_name = 'trends'))[0].translation)
    new = ucwords(word_list.filter(Q(var_name = 'new'))[0].translation)
    contra = ucwords(word_list.filter(Q(var_name = 'controversial'))[0].translation)
    rising = ucwords(word_list.filter(Q(var_name = 'rising'))[0].translation)
    best = ucwords(word_list.filter(Q(var_name = 'best'))[0].translation)
    now = ucwords(word_list.filter(Q(var_name = 'now'))[0].translation)
    today = ucwords(word_list.filter(Q(var_name = 'today'))[0].translation)
    thisweek = ucwords(word_list.filter(Q(var_name = 'this-week'))[0].translation)
    thismonth = ucwords(word_list.filter(Q(var_name = 'this-month'))[0].translation)
    thisyear = ucwords(word_list.filter(Q(var_name = 'this-year'))[0].translation)
    alltime = ucwords(word_list.filter(Q(var_name = 'all-time'))[0].translation)
    answerthequestions = ucwords(word_list.filter(Q(var_name = 'all-time'))[0].translation)
    discovernewtopics = ucwords(word_list.filter(Q(var_name = 'discover-more-communities'))[0].translation)
    morem = ucwords(word_list.filter(Q(var_name = 'more'))[0].translation)
    followmoreusers = ucwords(word_list.filter(Q(var_name = 'follow-more-users'))[0].translation)
    hiddentakeback = ucwords(word_list.filter(Q(var_name = 'hidden-take-back'))[0].translation)
    hiddenusers = ucwords(word_list.filter(Q(var_name = 'hidden-users'))[0].translation)
    media = ucwords(word_list.filter(Q(var_name = 'media'))[0].translation)
    link = ucwords(word_list.filter(Q(var_name = 'link'))[0].translation)
    quiz = ucwords(word_list.filter(Q(var_name = 'quiz'))[0].translation)
    poll = ucwords(word_list.filter(Q(var_name = 'poll'))[0].translation)
    question = ucwords(word_list.filter(Q(var_name = 'question'))[0].translation)
    feed_dict['trend'] = trend
    feed_dict['new'] = new
    feed_dict['contra'] = contra
    feed_dict['rising'] = rising
    feed_dict['best'] = best
    feed_dict['now'] = now
    feed_dict['today'] = today
    feed_dict['thisweek'] = thisweek
    feed_dict['thismonth'] = thismonth
    feed_dict['thisyear'] = thisyear
    feed_dict['alltime'] = alltime
    feed_dict['answerthequestions'] = answerthequestions
    feed_dict['discovernewtopics'] = discovernewtopics
    feed_dict['morem'] = morem
    feed_dict['followmoreusers'] = followmoreusers
    feed_dict['hiddentakeback'] = hiddentakeback
    feed_dict['hiddenusers'] = hiddenusers
    feed_dict['media'] = media
    feed_dict['link'] = link
    feed_dict['quiz'] = quiz
    feed_dict['poll'] = poll
    feed_dict['question'] = question
    return feed_dict

# Create your views here.
def home(request):
    current_uid = 8
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT meta_value FROM wpmu_usermeta WHERE user_id='{current_uid}' AND meta_key='language'")
    lang = mycursor.fetchone()[0]
    mycursor.execute("SELECT * FROM wpmu_usermeta WHERE user_id='{current_uid}' AND meta_key='mode'")
    dark = mycursor.fetchone()
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

    followed_communities = FollowedCommunities.objects.filter(Q(user_id = current_uid)).order_by('-date')[:10]
    followed_community_ids = list({x.term_id: x for x in followed_communities}.keys())
    followed_communities = Community.objects.filter(term_id__in=followed_community_ids)
    for i in followed_communities:
        i.name = ucwords(i.name)
    followed_communities_colors = CommunityMeta.objects.filter(term_id__in=followed_community_ids).filter(meta_key = 'color_up')
    for color in followed_communities_colors:
        if color.meta_value is None:
            color.meta_value = "var(--main-color)"
    followed_communities_url_ids = CommunityMeta.objects.filter(term_id__in=followed_community_ids).filter(meta_key = 'tag_img')
    followed_communities_url_ids = list({x.meta_value: x for x in followed_communities_url_ids}.keys())

    current_user = User.objects.filter(Q(ID = current_uid))[0]
    user_desc = UserMeta.objects.filter(Q(user_id = current_uid)).filter(Q(meta_key = 'description'))[0]
    current_user.set_description(user_desc.meta_value)
    mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{current_uid}')
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(current_uid) + "/" + onlyfiles[0]
    current_user.set_avatar(avatar_url)
    return render(request, 'index.html', {'lang':lang, 'dark':dark, 'current_user': current_user,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language,
                                            'followed_communities':followed_communities, 'followed_communities_colors':followed_communities_colors,
                                            'right_menu_dict':right_menu_dict, 'feed_dict':feed_dict
                                            })
