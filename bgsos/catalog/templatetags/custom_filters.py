# bgsos/catalog/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def cents_to_dollars(value):
    try:
        return value / 100
    except (ValueError, TypeError):
        return value
