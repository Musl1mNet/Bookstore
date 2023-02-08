from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    return list(i for i in range(len(number)))
@register.filter(name='get_itm')
def get_itm(obj, num):
    return obj[num] 