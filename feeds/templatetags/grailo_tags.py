from django import template
from django.template.defaultfilters import stringfilter
from textwrap import TextWrapper
import textwrap
import StringIO

register = template.Library()

@register.filter
def break_text(text, width):
    output = StringIO.StringIO()
    lines = textwrap.wrap(text,width=60)
    for line in lines:
        print >>output ,line

    return output.getvalue()
