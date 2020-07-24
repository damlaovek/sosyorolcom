from django import template
register = template.Library()

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
