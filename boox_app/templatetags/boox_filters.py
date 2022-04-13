from django import template

register = template.Library()

@register.filter
def range_of_int(value):
    return range(1, int(value))