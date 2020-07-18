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
