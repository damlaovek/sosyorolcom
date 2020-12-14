from django import template
import re
register = template.Library()

@register.filter
def getword(wordlist, db_key):
    return wordlist.get(var_name=db_key).translation

@register.filter
def isfollowing(followings, user):
    result = followings.filter(following=user)
    if result.count() > 0:
        return True
    else:
        return False

@register.filter
def getlist(indexable, i):
    j = 0
    for obj in indexable:
        if j==i:
            return {'name': obj.name, 'image':obj.photo_medium, 'url':obj.url}
        j += 1

@register.filter
def getdata(json, field):
    return json.get(field)

@register.filter
def tolower(txt):
    rep = [ ('İ','i'), ('I','ı'), ('Ğ','ğ'),('Ü','ü'), ('Ş','ş'), ('Ö','ö'),('Ç','ç')]
    for search, replace in rep:
        txt = txt.replace(search, replace)
    return txt.lower()

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

@register.filter
def toupper(txt):
    rep = [ ('İ','i'), ('I','ı'), ('Ğ','ğ'),('Ü','ü'), ('Ş','ş'), ('Ö','ö'),('Ç','ç')]
    for search, replace in rep:
        txt = txt.replace(replace, search)
    return txt.upper()

@register.filter
def ucfirst(txt):
    txt = tolower(txt)
    return toupper(txt[0]) + txt[1:]

@register.filter
def ucwords(txt):
    txt = tolower(txt)
    words = txt.split(" ")
    for i in range(0, len(words)):
        words[i] = ucfirst(words[i])
        subwords = words[i].split("/")
        for j in range(0, len(subwords)):
            subwords[j] = ucfirst(subwords[j])
        words[i] = "/".join(subwords)
    return " ".join(words)

@register.filter
def get_unit(number):
    number = int(number)
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

@register.filter
def edit_comm_desc(txt):
    txt = striphtml(txt)
    return txt[:156]