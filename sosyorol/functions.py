from PIL import Image
from resizeimage import resizeimage
import os
import time
import locale
import sosyorol.models as sm 
from django.db.models import Q
import datetime as dt
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as BSHTML
import operator


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
            try:
                new_instance = sm.CommunityCategoryRelation(community_id=c.term_id, category_id=category)
                new_instance.save()
            except:
                pass
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