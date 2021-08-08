from PIL import Image
from resizeimage import resizeimage
import os
from os import listdir
from os.path import isfile, join
import time
import locale
import sosyorol.models as sm 
from django.db.models import Q
import datetime as dt
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as BSHTML
import operator
import firebase_admin
from firebase_admin import auth, credentials, exceptions
import base64
import pandas as pd
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('turkish')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')


'''---------------------------------------
  STRING OPERATIONS              
-----------------------------------------'''
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

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

def change_special_chars(txt):
    removeSpecialChars = txt.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`\"~-=+"})
    removeSpecialChars = removeSpecialChars.translate ({ord(c): "" for c in "`'"})
    return removeSpecialChars

def correct_community_name(name):
    tokens = name.split(" ")
    name = localized_lower(tokens[0])
    tokens = [ucfirst(item) for item in tokens]
    name = ''.join(tokens)
    name = name.strip()
    name = change_special_chars(name)
    return name

def is_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True     
    else:  
        return False

'''---------------------------------------
  UNIT OPERATIONS            
-----------------------------------------'''
def get_unit(number):
    if number < 1000:
        return f"{number}"
    elif number >= 1000 & number < 1000000:
        return f"{number} K"
    elif number >= 1000000 & number < 1000000000:
        return f"{number} M"
    elif number >= 1000000000 & number < 1000000000000:
        return f"{number} B"
    else:
        return f"{number} T"


'''---------------------------------------
  DATE OPERATIONS        
-----------------------------------------'''
def humanizedate(date, word_list, to=None):
    sec_text = localized_lower(word_list.filter(var_name = 'sec')[0].translation)
    secs_text = localized_lower(word_list.filter(var_name = 'secs')[0].translation)
    min_text = localized_lower(word_list.filter(var_name = 'min')[0].translation)
    mins_text = localized_lower(word_list.filter(var_name = 'mins')[0].translation)
    hour_text = localized_lower(word_list.filter(var_name = 'hour')[0].translation)
    hours_text = localized_lower(word_list.filter(var_name = 'hours')[0].translation)
    day_text = localized_lower(word_list.filter(var_name = 'day')[0].translation)
    days_text = localized_lower(word_list.filter(var_name = 'days')[0].translation)
    week_text = localized_lower(word_list.filter(var_name = 'week')[0].translation)
    weeks_text = localized_lower(word_list.filter(var_name = 'weeks')[0].translation)
    month_text = localized_lower(word_list.filter(var_name = 'month')[0].translation)
    months_text = localized_lower(word_list.filter(var_name = 'months')[0].translation)
    year_text = localized_lower(word_list.filter(var_name = 'year')[0].translation)
    years_text = localized_lower(word_list.filter(var_name = 'years')[0].translation)
    ago = localized_lower(word_list.filter(var_name = 'ago')[0].translation)
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

def format_date(lang_code, date, format_string):
    locale.setlocale(locale.LC_TIME, lang_code)
    return time.strftime("%a, %d %b %Y %H:%M:%S")


'''---------------------------------------
  IMAGE OPERATIONS        
-----------------------------------------'''
def resize_image(filepath, typeOfImg):
    filepath = 'static/assets/' + filepath
    filename, file_extension = os.path.splitext(filepath)
    with open(filepath, 'r+b') as f:
        with Image.open(f) as image:
            if typeOfImg == "list":
                cover = resizeimage.resize_cover(image, [40, 40])
                cover.save(filename+"_40x40"+file_extension, image.format)
                cover = resizeimage.resize_cover(image, [60, 60])
                cover.save(filename+"_60x60"+file_extension, image.format)
                cover = resizeimage.resize_cover(image, [130, 130])
                cover.save(filename+"_130x130"+file_extension, image.format)
            elif typeOfImg == "community":
                cover = resizeimage.resize_cover(image, [40, 40])
                cover.save(filename+"_40x40"+file_extension, image.format)
                cover = resizeimage.resize_cover(image, [130, 130])
                cover.save(filename+"_130x130"+file_extension, image.format)
    return

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


'''---------------------------------------
  COMMUNITIES        
-----------------------------------------'''
def extract_categories():
    terms = sm.TermTaxonomy.objects.all()
    for term in terms:
        if term.taxonomy == "category":
            try:
                print("term id: "+str(term.term_id))
                category = sm.Community.objects.filter(Q(term_id=term.term_id))[0]
                new_category = sm.CommunityCategories(term_id=category.term_id, name=category.name)
                new_category.save()
            except:
                pass

def find_category(community, category_ids=None):
    if category_ids is None:
        category_ids = sm.CommunityCategories.objects.all()
        category_ids = list({x.term_id: x for x in category_ids}.keys())
    cat_dct = {}
    print(f"Start searching for the category of {community.name}")
    transform_dct = {34:9, 8814:51, 6195:8647, 8681:8, 10857:8, 12071:119, 3067:119}
    if community.term_id in category_ids:
        print(f"{community.term_id} is already a category")
        return community.term_id
    try:
        term_taxonomy = sm.TermTaxonomy.objects.get(term_id=community.term_id)
        posts = sm.TermRelationship.objects.filter(Q(term_taxonomy_id=term_taxonomy.term_taxonomy_id))
        print(f"There are {len(posts)} posts to be examined")
        for p in posts:
            objects = sm.TermRelationship.objects.filter(Q(object_id=p.object_id))
            for o in objects:
                try:
                    term_id = sm.TermTaxonomy.objects.get(term_taxonomy_id=o.term_taxonomy_id)
                    if term_id.term_id in transform_dct.keys():
                        cid = transform_dct[term_id.term_id]
                    else:
                        cid = term_id.term_id
                    if cid != community.term_id and cid in category_ids:
                        if cid in cat_dct.keys():
                            cat_dct[cid] = cat_dct[cid] + 1
                        else:
                            cat_dct[cid] = 1
                except:
                    pass
    except:
        pass
    if not bool(cat_dct):
        print(f"No category found for {community.term_id}")
        return -1
    else:
        print(cat_dct)
        return max(cat_dct,  key=cat_dct.get)

def find_category_of_community():
    category_ids = sm.CommunityCategories.objects.all()
    category_ids = list({x.term_id: x for x in category_ids}.keys())
    communities = sm.Community.objects.all()
    for c in communities:
        category = find_category(c, category_ids)
        print(f"Category for {c.term_id} is {category}")
        if category > 0:
            new_instance = sm.CommunityCategoryRelation(community_id=c.term_id, category_id=category, relation=0)
            new_instance.save()
    return

def generate_descriptions():
    communities = sm.Community.objects.all()
    for c in communities:
        try:
            meta_desc = sm.YoastMetaFields.objects.get(object_id=c.term_id).description
            c.description = meta_desc
            c.save()
            print(meta_desc)
        except:
            pass
    return

def get_date_created():
    communities = sm.Community.objects.all()
    for c in communities:
        try:
            date_created = sm.CommunityMeta.objects.filter(Q(term_id=c.term_id))
            #c.update(date_created=date_created.meta_value)
            print(len(date_created))
        except:
            pass
    return

def find_similar_communities(community, user):
    taxonomies = sm.TermTaxonomy.objects.filter(term_id=community.term_id)
    post_ids = sm.TermRelationship.objects.filter(term_taxonomy_id__in=taxonomies)
    post_ids = list({x.object_id: x for x in post_ids}.keys())
    posts = sm.Post.objects.filter(ID__in=post_ids)
    similars = []
    for post in posts:
        community_taxonomy_ids = sm.TermRelationship.objects.filter(object_id=post.ID)
        community_taxonomy_ids = list({x.term_taxonomy_id: x for x in community_taxonomy_ids}.keys())
        community_ids = sm.TermTaxonomy.objects.filter(term_taxonomy_id__in=community_taxonomy_ids)
        community_ids = list({x.term_id: x for x in community_ids if x.term_id != community.term_id}.keys())
        comms = sm.Community.objects.filter(term_id__in=community_ids)
        for c in comms:
            if not c in similars:
                if sm.FollowedCommunities.objects.filter(user=user, term=c, is_active=1).count() == 0:
                    similars.append(c)
    return similars

'''---------------------------------------
  TRANSFER USERS TO FIREBASE        
-----------------------------------------'''
def transferUsers():
    if not firebase_admin._apps:
        cred = credentials.Certificate('static/sosyorol-b6ab6-firebase-adminsdk-q80t3-54150f4057.json') 
        default_app = firebase_admin.initialize_app(cred)
    userObjects = sm.User.objects.all()
    users = []
    '''
    for u in userObjects:
        users.append('sosyoroluseruid'+str(u.ID))
    result = auth.delete_users(users)
    '''
    for u in userObjects:
        pass_hash = str.encode(u.user_pass)
        user = auth.ImportUserRecord(uid='sosyoroluseruid'+str(u.ID), email=u.user_email, password_hash=pass_hash)
        users.append(user)
    hash_alg = auth.UserImportHash.md5(rounds=0)
    try:
        result = auth.import_users(users, hash_alg=hash_alg)
        for err in result.errors:
            print('Failed to import user:', err.reason)
    except exceptions.FirebaseError as error:
        print('Error importing users:', error)


'''---------------------------------------
  USERS        
-----------------------------------------'''
def arrange_usernames():
    users = sm.User.objects.all()
    for user in users:
        username = user.user_login.replace(".","_")
        user.user_login = username
        user.save()

def read_langs():
    xls = pd.ExcelFile('sosyorol/diller.xlsx')
    df1 = pd.read_excel(xls, 'Sheet1')
    df2 = pd.read_excel(xls, 'Sheet2')
    df3 = pd.read_excel(xls, 'Sheet3')

    for index, row in df1.iterrows():
        #new_lang = sm.Languages(var_name="lang-ns-"+str(index), lang_code="tr-TR", translation=row["TR"])
        #new_lang.save()
        new_lang = sm.Languages(var_name="lang-ns-"+str(index), lang_code="en-EN", translation=row["EN"])
        new_lang.save()
        new_lang = sm.Languages(var_name="lang-ns-"+str(index), lang_code="de-DE", translation=row["DE"])
        new_lang.save()

def profile_pictures():
    users = sm.User.objects.all()
    for user in users:
        mypath = os.path.join(STATICFILES_DIR, f'assets/img/user_avatars/{user.ID}')
        if (os.path.exists(mypath)):
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            if len(onlyfiles) > 0:
                avatar_url = "https://www.sosyorol.com/wp-content/uploads/avatars/" + str(user.ID) + "/" + onlyfiles[0]
            else:
                avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        else:
            avatar_url = "https://www.gravatar.com/avatar/655e8d8d32f890dd8b07377a74447a5c?s=150&r=g&d=mm"
        new_cred = sm.UserMeta(user=user, meta_key="avatar_url", meta_value=avatar_url)
        new_cred.save()

def get_birthdays():
    birthday_data = sm.UserData.objects.filter(field_id=2)
    for bd in birthday_data:
        try:
            new_data = sm.UserMeta(user=bd.user, meta_key="birthday", meta_value=bd.value)
            new_data.save()
        except:
            pass

def updatecommunityslugs():
    communities = sm.Community.objects.all()
    for c in communities:
        slug = c.slug
        slug = slug.replace("ı", "i")
        slug = slug.replace("ğ", "g")
        slug = slug.replace("ş", "s")
        slug = slug.replace("ç", "c")
        slug = slug.replace("ö", "o")
        slug = slug.replace("ü", "u")
        c.slug = slug
        c.save()

def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

def computePostDistances():
    posts = sm.Post.objects.filter(post_status="publish", post_type__in=["post", "quiz", "poll", "answer", "questions", "link", "media"]).order_by("ID")
    for post in posts:
        others = sm.Post.objects.filter(ID__gte=post.ID).order_by("ID")
        for other in others:
            if post.ID != other.ID:
                sentences = [post.post_title, other.post_title]
                cleaned = list(map(clean_string, sentences))
                vectorizer = CountVectorizer().fit_transform(cleaned)
                vectors = vectorizer.toarray()
                similarity = cosine_sim_vectors(vectors[0], vectors[1])
                try:
                    print(f"Similarity btw {post.ID} and {other.ID} is {similarity}")
                    new_sim = sm.SimilarPosts(post1=post, post2=other, similarity=similarity)
                    new_sim.save()
                except:
                    pass

def calculate_community_score():
    communities = sm.Community.objects.all()
    for community in communities:
        print(f"Calculating score for c/{community.name}")
        taxonomy = sm.TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
        post_ids = sm.TermRelationship.objects.filter(Q(term_taxonomy_id=taxonomy))
        post_ids = list({x.object_id: x for x in post_ids}.keys())
        community.posts = sm.Post.objects.filter(Q(ID__in=post_ids)).order_by('-post_date')
        num_posts = community.posts.filter(post_type="post").count()

def update_post_authors():
    authors = [7,8,49,86,209,267]
    posts = sm.Post.objects.all()
    index = 0
    for post in posts:
        if post.post_author not in authors:
            if index % 2 == 0:
                post.post_author = 209
            else:
                post.post_author = 267
            post.author_id = post.post_author
            post.save()
        index += 1

def update_post_history():
    posts = sm.Post.objects.filter(post_status="publish")
    for post in posts:
        try:
            view_count = int(sm.PostMeta.objects.filter(post_id=post.ID, meta_key="post_views_count")[0].meta_value)
            history = sm.PostHistory(user_id=-1, post_id=post.ID, date=dt.datetime.now(), is_deleted=0, counter=view_count)
            history.save()
        except:
            pass

def update_community_views():
    communities = sm.Community.objects.all()
    for community in communities:
        try:
            taxonomy = sm.TermTaxonomy.objects.filter(term_id=community.term_id)[0].term_taxonomy_id
            post_ids = sm.TermRelationship.objects.filter(term_taxonomy_id=taxonomy)
            post_ids = list({x.object_id: x for x in post_ids}.keys())
            community.posts = sm.Post.objects.filter(ID__in=post_ids).order_by('-post_date')
            view_count = 0
            for post in community.posts:
                try:
                    view_count += int(sm.PostMeta.objects.filter(post_id=post.ID, meta_key="post_views_count")[0].meta_value)
                except:
                    pass
            community.views = view_count
            community.save()
        except:
            pass
        
def update_community_followers():
    followers = sm.FollowedCommunities.objects.all()
    for f in followers:
        try:
            user = sm.User.objects.filter(ID=f.user_id)
            if len(user) == 0:
                f.delete()
        except:
            f.delete()

def update_followers():
    all = sm.UserRelation.objects.all()
    for query in all:
        try:
            following = sm.User.objects.get(ID=query.following_id)
            try:
                follower = sm.User.objects.get(ID=query.follower_id)
            except:
                query.delete()
        except:
            query.delete()

