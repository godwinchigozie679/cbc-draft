from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, FormView
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
  

  
  

# Main Video Page
@login_required(login_url='login')
def video(request, slug): 
    course = Course.objects.get(slug=slug)
    
    
    # Course Raview
    course_reviews = Review.objects.filter(course=course)[0:4]
    
    # I Used this to check for Updata
    review = Review.objects.filter(course=course)
    
      
    # Average Rating
    average_course_review = Review.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']
    
    # Enrolled
    is_enrolled = course  
       
    modules = Modulee.objects.filter(course=course,)  #Logic for next and previous video
    for module in modules:
        module = module
        for quiz in module.course_module_quiz.filter(course=course):
            quiz = quiz
            for result in quiz.quiz_result.filter(user=request.user, quiz__course=course):
                result = result
                
              
    
    
             
    
    
    serial_number = request.GET.get('lecture')      
   
    if serial_number is None:
        serial_number = 1
        
    
    # video.user_course = course
    videos = Video.objects.filter(serial_number = serial_number, course = course,)
    for video in videos:
        video = video 
    
    try:
        if video.is_preview == False:        
            if (request.user.is_authenticated == False):
                return redirect('login')
            else:
                try:  
                    #IF USER IS PAID AND CONFIRMED CHANGE ALL COURSE PREVIEW TO TRUE
                    if video.is_preview == False:
                        user = request.user
                        user_courses = UserCourse.objects.filter(course=course, user=user)
                        for user_course in user_courses:
                            user_course = user_course   
                        
                        payment = Payment.objects.filter(user=user, course=course)
                        for pay in payment:
                            pay = pay       
                        
                        if user_course and pay.verified == True:
                            video.is_preview = True                        
                            video.save()
                        
                                                
                except:
                    return redirect('checkout', slug)
    except:
        return HttpResponse('Page Can not be found') 
    
    context = { "course": course,
                "video": video, 
                "modules": modules,  
                'is_enrolled': is_enrolled,  
                "course_reviews": course_reviews,  
                'average_course_review': average_course_review,    
                'review': review,            
              
               }   
    
    return render(request, template_name="courses/video.html", context=context)

