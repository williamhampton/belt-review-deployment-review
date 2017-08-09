from django import template

register = template.Library()

@register.assignment_tag
def adding(val1, val2):
    val1 = val1 + val2;
    return val1;
@register.assignment_tag
def subtracting(val1, val2):
    val1 = val1 - val2;
    return val1;
