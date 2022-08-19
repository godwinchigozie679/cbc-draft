from django import template
from social_handle.models import SocialHandle, PhoneNumber, Email, OfficeAdress
from blog.models import Post
from e_learning.models.sector import Sector


from django.template.loader import get_template
register = template.Library()

@register.inclusion_tag('footer.html')
def show_footer():
    phone_number    = PhoneNumber.objects.all()[0]
    email_address   = Email.objects.all()[0]
    social_address  = SocialHandle.objects.all()
    office_address  = OfficeAdress.objects.all()[0] 
    post            = Post.blog_published.all()[0]
    

    
    
    return {'phone_number': phone_number,
            'email_address': email_address,
            'social_address': social_address,
            'office_address': office_address,
            'post': post}





