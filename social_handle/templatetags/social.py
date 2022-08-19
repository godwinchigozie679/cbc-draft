from django import template
from social_handle.models import SocialHandle


from django.template.loader import get_template
register = template.Library()

@register.inclusion_tag('social.html')
def social():
    social_handle = SocialHandle.objects.all() 
       
    return {'social_handle': social_handle,}


