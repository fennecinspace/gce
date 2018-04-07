from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='second_zero_adder')
@stringfilter
def second_zero_adder(value):
    if len(value) == 1:
        value = '0' + value 
    return value