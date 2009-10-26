import urlparse
from django.utils.encoding import iri_to_uri
from django.conf import settings
from django.core import urlresolvers
from shorturls.baseconv import base62

class PrefixMap():
    def __init__(self):
        self.prefixmap = dict((m,p) for p,m in settings.SHORTEN_MODELS.items())

    def get_prefix(self, obj):
        key = '%s.%s' % (obj._meta.app_label, obj.__class__.__name__.lower())
        return self.prefixmap[key]

prefixmap = PrefixMap()

def shortify(obj):
    prefix = prefixmap.get_prefix(obj)
    
    tinyid = base62.from_decimal(obj.pk)
    
    if hasattr(settings, 'SHORT_BASE_URL') and settings.SHORT_BASE_URL:
        return settings.SHORT_BASE_URL+prefix+tinyid
        
        try:
            return urlresolvers.reverse('shorturls.views.redirect', kwargs = {
                'prefix': prefix,
                'tiny': tinyid
            })
        except urlresolvers.NoReverseMatch:
            return ''