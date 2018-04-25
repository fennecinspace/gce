from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='second_zero_adder')
@stringfilter
def second_zero_adder(value):
    values = value.split('.')

    if len(values[0]) == 1:
        values[0] = '0' + values[0] 

    if len(values[1]) == 1:
            values[1] = values[1] + '0'


    value = '.'.join(values)
    return value


@register.filter(name='none_to_empty')
def none_to_empty(value):
    if value == None:
        return ""
    return value

    