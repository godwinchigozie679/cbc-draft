from django import template
import math
from e_learning.models.course import Course
from e_learning.models.user_course import UserCourse
from e_learning.models.course_review import Review
from django.db.models import Avg
from e_learning.models.course_modules import Modulee
from e_learning.models.quiz import Question, Result



register = template.Library()

@register.simple_tag
def cal_main_price(price, percentage_discount):    
    
    if percentage_discount == None or percentage_discount == 0 or price == 0:
        return price
    else:
        selling_price = price        
        new_selling_price = selling_price - (price * percentage_discount * 0.01)
        return math.floor(new_selling_price)
    
    

@register.filter
def dollar(price):
    return f'${price}'




@register.simple_tag
def is_enrolled(request, course): 
        
    # user = None
    # if not request.user.is_authenticated:
    #     return False
    
    # user = request.user    
    try:  
        user = request.user                        
        user_course = UserCourse.objects.get(course=course, user=user) 
         
        return True                              
    except:
        return False


