from PIL import Image
from resizeimage import resizeimage
import os
import time
import locale
from sosyorol.models import *

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

# Resize list image
def resize_list_image(filepath):
    filepath = 'static/assets/' + filepath
    filename, file_extension = os.path.splitext(filepath)
    with open(filepath, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [40, 40])
            cover.save(filename+"_40x40"+file_extension, image.format)
            cover = resizeimage.resize_cover(image, [60, 60])
            cover.save(filename+"_60x60"+file_extension, image.format)
            cover = resizeimage.resize_cover(image, [130, 130])
            cover.save(filename+"_130x130"+file_extension, image.format)
    return

def format_date(lang_code, date, format_string):
    locale.setlocale(locale.LC_TIME, lang_code)
    return time.strftime("%a, %d %b %Y %H:%M:%S")


def change_special_chars(txt):
    removeSpecialChars = txt.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`\"~-=+"})
    removeSpecialChars = removeSpecialChars.translate ({ord(c): "" for c in "`'"})
    return removeSpecialChars


def manipulate_communities():
    communities = Community.objects.all()
    for community in communities:
        name = community.name
        tokens = name.split(" ")
        name = localized_lower(tokens[0])
        for i in range(1, len(tokens)):
            name += ucfirst(tokens[i])
        name = name.strip()
        name = change_special_chars(name)
        community.name = name
        community.slug = name
        community.save()



