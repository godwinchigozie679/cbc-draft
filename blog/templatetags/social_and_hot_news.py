from django import template
from django.http import HttpResponse
from social_handle.models import SocialHandle
from blog.models import NewsPost

from django.template.loader import get_template
register = template.Library()

@register.inclusion_tag('custom_tag_templates/social_and_hot_news.html')
def social_and_hot_news():
    
    try:
        social_handle = SocialHandle.objects.all()
        all_news = NewsPost.news_published.all() 
        
        return {'social_handle': social_handle,
            'all_news': all_news,
            }
    except Exception:
        return HttpResponse('Page Can not be found')
    
    
    


