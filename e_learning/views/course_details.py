from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, FormView
from account.models import Account
from django.http import HttpResponse
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from e_learning.models.video import Video
from e_learning.models.user_course import UserCourse
from payment.models import Payment
from e_learning.models.course_review import Review
from django.db.models import Avg
from e_learning.models.sector import Sector
from e_learning.models.quiz import Result
#Login Decorator
from django.contrib.auth.decorators import login_required



#######################################################################################
  

def course_details(request, slug):   
   
   try:
       course = Course.objects.get(slug=slug)
       
       #Related Course
       course_tag = course.tags.all()
       related_courses = Course.objects.filter(active=True, tags__in = course_tag).exclude(slug=slug)
       
       # Getting Author
       course_id = course.id
       author_ = Account.objects.filter(author_course__id=course_id)
       author_name = author_[0]
       
       # All Course by Author
       author_course = Course.objects.filter(author=author_name)
       
       # Author Lectures
       author_lectures = Modulee.objects.filter(course__author=author_name)
       
       # All Student Enrolled
       author_enrolled_students = UserCourse.objects.filter(course__author=author_name)
       
       # Course Raview
       course_reviews = Review.objects.filter(course=course)[0:4]
       
       # I Used this to check for Updata
       review = Review.objects.filter(course=course)
       
      
       
       # Average Rating               
       average_course_review = Review.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']
       
       
       # Rating
       total_rating = 5.0
       star_5 = Review.objects.filter(course__slug=slug, rating__gte=4.5).aggregate(Avg('rating'))['rating__avg']
       star_4 = Review.objects.filter(course__slug=slug, rating__gte=4.0, rating__lt=4.5).aggregate(Avg('rating'))['rating__avg']
       star_3 = Review.objects.filter(course__slug=slug, rating__gte=3.0, rating__lt=4.0).aggregate(Avg('rating'))['rating__avg']
       star_1 = Review.objects.filter(course__slug=slug, rating__lt=3.0).aggregate(Avg('rating'))['rating__avg']
   
       # star 5
       if star_5 is not None:
           star_5_percent = star_5/total_rating * 100
       else:
           star_5_percent = 0.0
       
       # star 4
       if star_4 is not None:
           star_4_percent = star_4/total_rating * 100
       else:
           star_4_percent = 0.0
       
       # star 3
       if star_3 is not None:
           star_3_percent = star_3/total_rating * 100
       else:
           star_3_percent = 0.0
   
        # star 1 
       if star_1 is not None:
           star_1_percent = star_1/total_rating * 100
       else:
           star_1_percent = 0.0
   

   except:       
       return HttpResponse('Page Can not be found')
   
   context = {
       'course': course,
       'author_course':author_course,
       'author_lectures':author_lectures,
       'author_enrolled_students': author_enrolled_students,
       'related_courses': related_courses,
       "course_reviews": course_reviews,  
        'average_course_review': average_course_review,    
        'review': review,
        'star_5_percent': str(format(star_5_percent, ".0f"))+'%',
        'star_4_percent': str(format(star_4_percent, ".0f"))+'%',
        'star_3_percent': str(format(star_3_percent, ".0f"))+'%',
        'star_1_percent': str(format(star_1_percent, ".0f"))+'%',
                      
       
       }
   
   
   return render(request, template_name='courses/course_details.html', context=context)
  
