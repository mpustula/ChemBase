from django import template
#from urllib.parse import urlencode
import urllib.parse

register=template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    #print(query)
    query.update(kwargs)
    #print(urllib.parse.urlencode(query))
    return urllib.parse.urlencode(query) 
