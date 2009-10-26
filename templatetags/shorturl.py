import urlparse

from django import template
from django.core import urlresolvers
from django.utils.safestring import mark_safe

from shorturls.baseconv import base62
from shelfurls.functions import shortify

class ShortURL(template.Node):
    @classmethod
    def parse(cls, parser, token):
        parts = token.split_contents()
        if len(parts) != 2:
            raise template.TemplateSyntaxError("%s takes exactly one argument" % parts[0])
        return cls(template.Variable(parts[1]))
    
    def __init__(self, obj):
        self.obj = obj
    
    def render(self, context):
        try:
            obj = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        return shortify(obj)

class RevCanonical(ShortURL):
    def render(self, context):
        url = super(RevCanonical, self).render(context)
        if url:
            return mark_safe('<link rev="canonical" href="%s">' % url)
        else:
            return ''

register = template.Library()
register.tag('shorturl', ShortURL.parse)
register.tag('revcanonical', RevCanonical.parse)