from django import template

register = template.Library()

@register.tag
def django_mustache(parser, token):
    nodelist = parser.parse(('end_django_mustache',))
    parser.delete_first_token()
    return DjangoMustache(nodelist)

class DjangoMustache(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context, ):
        output = self.nodelist.render(context)
        return output.replace('[[', '{{').replace(']]', '}}')