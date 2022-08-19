from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.http import HttpResponse
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from e_learning.models.video import Video
from e_learning.models.user_course import UserCourse




#Login Decorator
from django.contrib.auth.decorators import login_required

####################################################################################### 
  




def course_author_profile(request, slug):
    course_author_profile = Course.objects.get(slug=slug)
    context = {    
        "course_author_profile":course_author_profile,    
    }
    
    return render(request, template_name='courses/author_profile.html', context=context)


