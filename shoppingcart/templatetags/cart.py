from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    if arg:
        return value - arg
    return value
