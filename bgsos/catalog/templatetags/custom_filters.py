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


@register.filter
def divisibleby(value, divisor):
    try:
        return value / divisor
    except (ValueError, ZeroDivisionError, TypeError):
        return value

@register.filter
def format_float(value):
    return f"{value:.2f}"

@register.filter
def cents_to_points(value):
    try:
        return value / 10000
    except (ValueError, TypeError):
        return value
