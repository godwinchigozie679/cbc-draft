from django.contrib import admin
from django.urls import path, include
#Mapping of Homepage from view
from e_learning.views import  homepage, course_video, user_course, course_page, course_details, all_course_in_category, review, course_author_profile, quiz





urlpatterns = [    
    path('', homepage.HOME.as_view(), name='home'), 
    path('home-filter-data', homepage.home_filter_data, name='home-filter-data'),  
     
    # All Course
    path('courses/', course_page.CoursePage.as_view(), name ='course_page'),
    # Filter
    path('course-page-filter', course_page.CoursePageFilter.as_view(), name='course-page-filter'),
    
    
    
    # Category
    path('category/<str:slug>', all_course_in_category.CategoryCourse.as_view(), name ='category_course'),
    # Category Filter Data
    path('category-filter', all_course_in_category.CourseCategoryFilter.as_view(), name='category-filter'),
    # Main Course
    path('courses/<slug:slug>', course_video.video, name ='main_course'),
    # Course Course Detail
    path('courses-details/<slug:slug>', course_details.course_details, name ='course_details'),
    # User Course for Payment and other verification
    path('account/', user_course.user_course, name ='user_course'),
    path('course_success_payment/<slug:slug>', user_course.course_success_payment, name ='course_success_payment'),
    # Review
    path('submit_review/<slug:slug>', review.submit_review, name ='submit_review'),
    path('all_review/<slug:slug>', review.all_review, name ='all_review'),
    
    # course-author_profile
    path('profile/<slug:slug>', course_author_profile, name ='course_author_profile'),
    
    # Quiz
    path('course_quiz/<slug:slug>/<int:pk>', quiz.course_quiz, name ='quiz'),
    path('course_quiz/<slug:slug>/<int:pk>/data', quiz.course_quiz_data, name ='quiz_data'),
    path('course_quiz/<slug:slug>/<int:pk>/save_data', quiz.course_quiz_save, name ='quiz_save'),
    
] 


