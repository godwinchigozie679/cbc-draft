from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.http import HttpResponse
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from e_learning.models.video import Video
from e_learning.models.user_course import UserCourse
from e_learning.models.quiz import Result
from e_learning.views import  homepage, course_video, user_course, course_page

# Paginator
from django.core.paginator import Paginator

#Login Decorator
from django.contrib.auth.decorators import login_required

#######################################################################################
@login_required(login_url='login')
def course_success_payment(request, slug):
    user = request.user
    user_bought_course = UserCourse.objects.get(user=user, course__slug=slug)
    slug = user_bought_course.course.slug
    course = Course.objects.get(slug=slug)
    modules = Modulee.objects.filter(course=course,)  #Logic for next and previous video
    for module in modules[:1]:
        module = module
        for quiz in module.course_module_quiz.filter(course=course):
            quiz = quiz
    module_score = module.module_quiz_pass_mark
    # Access to module 1 of course
    Result.objects.create(quiz=quiz, user=request.user, score=module_score, module=module)
    
        
    
    context = {
     'user_bought_course':user_bought_course,
     'slug': slug,   
    }
    
    return render(request, template_name='courses/dashboard/student-dashboard/success_course_payment.html', context=context) 
  

# Main Video Page
@login_required(login_url='login')
def user_course(request):   
    user = request.user
                    
    user_course_list = UserCourse.objects.filter(user=user) 
    
    
    # set up paginator
    
    paginator = Paginator(user_course_list, 4)
    page = request.GET.get('page')
    user_courses = paginator.get_page(page)
    
    # Paginator number of page (next and prev)
    nums = 'a' * user_courses.paginator.num_pages
    
    context = {
        'user_courses': user_courses,
        'user': user,
        'nums':nums,
        
               }   
    
    return render(request, template_name="courses/dashboard/student-dashboard/my_paid_courses.html", context=context)




