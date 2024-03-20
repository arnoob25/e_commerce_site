"""registers custom filters"""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """functions as zip"""
    return dictionary.get(key)
