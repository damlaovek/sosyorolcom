from django.shortcuts import render
from django.http import HttpResponse
from sosyorol.models import *
import mysql.connector
from django.db.models import Q

mydb = mysql.connector.connect(
    host="185.87.252.147",
    user="dmlssyrl",
    passwd="190734fB@vesselam",
    database="unhelvasi_wp864"
)
def ucfirst(txt):
    return txt[0].upper() + txt[1:]

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


# Create your views here.
def home(request):
    current_uid = 8
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT meta_value FROM wpmu_usermeta WHERE user_id='8' AND meta_key='language'")
    lang = mycursor.fetchone()[0]
    mycursor.execute("SELECT * FROM wpmu_usermeta WHERE user_id='{current_uid}' AND meta_key='mode'")
    dark = mycursor.fetchone()
    word_list = Languages.objects.filter(Q(lang_code = lang))
    header_dict = header(word_list)
    left_menu_dict = left_menu(word_list)
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
    followed_communities_colors = CommunityMeta.objects.filter(term_id__in=followed_community_ids).filter(meta_key = 'color_up')
    for color in followed_communities_colors:
        if color.meta_value is None:
            color.meta_value = "var(--main-color)"
    followed_communities_url_ids = CommunityMeta.objects.filter(term_id__in=followed_community_ids).filter(meta_key = 'tag_img')
    followed_communities_url_ids = list({x.meta_value: x for x in followed_communities_url_ids}.keys())

    '''
    $interaction = $wpdb->get_results("SELECT * FROM languages WHERE var_name='interaction' AND lang_code='$lang'")[0]->translation;
    $scrollToTop = $wpdb->get_results("SELECT * FROM languages WHERE var_name='scroll-to-top' AND lang_code='$lang'")[0]->translation;
    $viewProfile = $wpdb->get_results("SELECT * FROM languages WHERE var_name='go-to-profile' AND lang_code='$lang'")[0]->translation;
    $trend = $wpdb->get_results("SELECT * FROM languages WHERE var_name='trends' AND lang_code='$lang'")[0]->translation;
    $new = $wpdb->get_results("SELECT * FROM languages WHERE var_name='new' AND lang_code='$lang'")[0]->translation;
    $contra = $wpdb->get_results("SELECT * FROM languages WHERE var_name='controversial' AND lang_code='$lang'")[0]->translation;
    $rising = $wpdb->get_results("SELECT * FROM languages WHERE var_name='rising' AND lang_code='$lang'")[0]->translation;
    $best = $wpdb->get_results("SELECT * FROM languages WHERE var_name='best' AND lang_code='$lang'")[0]->translation;
    $now = $wpdb->get_results("SELECT * FROM languages WHERE var_name='now' AND lang_code='$lang'")[0]->translation;
    $today = $wpdb->get_results("SELECT * FROM languages WHERE var_name='today' AND lang_code='$lang'")[0]->translation;
    $thisWeek = $wpdb->get_results("SELECT * FROM languages WHERE var_name='this-week' AND lang_code='$lang'")[0]->translation;
    $thisMonth = $wpdb->get_results("SELECT * FROM languages WHERE var_name='this-month' AND lang_code='$lang'")[0]->translation;
    $thisYear = $wpdb->get_results("SELECT * FROM languages WHERE var_name='this-year' AND lang_code='$lang'")[0]->translation;
    $allTime = $wpdb->get_results("SELECT * FROM languages WHERE var_name='all-time' AND lang_code='$lang'")[0]->translation;
    $answerTheQuestions = $wpdb->get_results("SELECT * FROM languages WHERE var_name='answer-the-questions' AND lang_code='$lang'")[0]->translation;
    $discoverNewTopics = $wpdb->get_results("SELECT * FROM languages WHERE var_name='discover-more-communities' AND lang_code='$lang'")[0]->translation;
    $morem = $wpdb->get_results("SELECT * FROM languages WHERE var_name='more' AND lang_code='$lang'")[0]->translation;
    $followMoreUsers = $wpdb->get_results("SELECT * FROM languages WHERE var_name='follow-more-users' AND lang_code='$lang'")[0]->translation;
    $hiddenTakeBack = $wpdb->get_results("SELECT * FROM languages WHERE var_name='hidden-take-back' AND lang_code='$lang'")[0]->translation;
    $hiddenUsers = $wpdb->get_results("SELECT * FROM languages WHERE var_name='hidden-users' AND lang_code='$lang'")[0]->translation;
    $media = $wpdb->get_results("SELECT * FROM languages WHERE var_name='media' AND lang_code='$lang'")[0]->translation;
    $link = $wpdb->get_results("SELECT * FROM languages WHERE var_name='link' AND lang_code='$lang'")[0]->translation;
    $quiz = $wpdb->get_results("SELECT * FROM languages WHERE var_name='quiz' AND lang_code='$lang'")[0]->translation;
    $poll = $wpdb->get_results("SELECT * FROM languages WHERE var_name='poll' AND lang_code='$lang'")[0]->translation;
    $question = $wpdb->get_results("SELECT * FROM languages WHERE var_name='question' AND lang_code='$lang'")[0]->translation;
    '''
    return render(request, 'index.html', {'lang':lang, 'dark':dark, 'current_uid': current_uid,
                                            'header_dict':header_dict, 'left_menu_dict':left_menu_dict,
                                            'country_list':country_list, 'select_language':select_language
                                            })
