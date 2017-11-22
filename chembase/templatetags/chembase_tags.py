from django import template
#from urllib.parse import urlencode
import urllib.parse
from chembase.models import Compound

register=template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    #print(query)
    query.update(kwargs)
    #print(urllib.parse.urlencode(query))
    return urllib.parse.urlencode(query) 

@register.simple_tag
def allowed_items_number(user,compound):
    
    existing_items=compound.item_set(manager='citems').existing()
    allowed_existing=compound.item_set(manager='citems').allowed(user,existing_items)
    
    item_num=len(allowed_existing)
    
    if item_num>1:
        return '%d'%item_num+' items available'
    elif item_num==1:
        return '%d'%item_num+' item available'
    else:
        return 'No items available'
    
@register.simple_tag
def allowed_items_list(user,compound):
    
    existing_items=compound.item_set(manager='citems').existing()   
    allowed_existing=compound.item_set(manager='citems').allowed(user,existing_items)
    
    result_list=[x['a'].local for x in allowed_existing]
    
    result_list=[]
    for item in allowed_existing:
        annot=''
        if item['a'].annotation_set.all():
            for ann in item['a'].annotation_set.all():
                annot=annot+ann.annotation+', '
            result_list.append(item['a'].local+' ('+annot+')')
        else:
            result_list.append(item['a'].local)
    
    #print(result_list)
    
    return ', '.join(result_list)
    

