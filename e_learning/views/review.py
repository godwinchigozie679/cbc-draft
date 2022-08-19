from e_learning.models.course_review import Review
from e_learning.models.course_forms import ReviewForm
from e_learning.models.course import Course
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from e_learning.models.user_course import UserCourse
from django.contrib import messages
from django.db.models import Avg

# Import Paginator
from django.core.paginator import Paginator



@login_required(login_url='login')
def submit_review(request, slug):
    user = request.user
    course = Course.objects.get(slug=slug,)
    user_course = UserCourse.objects.filter(course=course, user=user) 
    url = request.META.get('HTTP_REFERER')
    
    try:
        if request.method == 'POST':
            
            reviews = Review.objects.get(course=course, user_id=request.user.id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, your review has been updated.')
            return redirect(url)
            
                            
    except Review.DoesNotExist:
        if user_course:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.rating = form.cleaned_data['rating']
                data.comment = form.cleaned_data['comment']
                data.ip = request.META.get('REMOTE_ADDR')
                data.course = course
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, your review has been submitted.')
                return redirect(url)
               
        return redirect('checkout', slug)




# ALL REVIEW #################################################################################
@login_required(login_url='login')
def all_review(request, slug):
    
    
    course = Course.objects.get(slug=slug)
    # Course Raview
    course_review_list = Review.objects.filter(course=course)
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
    
    
    # set up paginator
    
    paginator = Paginator(course_review_list, 8)
    page = request.GET.get('page')
    course_reviews = paginator.get_page(page)
    
    # Paginator Next and Previous Pages
    nums = 'a' * course_reviews.paginator.num_pages
    
    # I used this to post to get course so user can create and update review
    review = Review.objects.filter(course=course)
    
    user = request.user
    course = Course.objects.get(slug=slug,)
    user_course = UserCourse.objects.filter(course=course, user=user) 
    url = request.META.get('HTTP_REFERER')
    
    try:
        if request.method == 'POST':
            
            reviews = Review.objects.get(course=course, user_id=request.user.id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            # Updating course rating average and comment_count field
            course.rating_average = average_course_review
            course.comment_count = Review.objects.filter(course=course).count()
            course.save()
            messages.success(request, 'Thank you, your review has been updated.')
            return redirect(url)
            
                            
    except Review.DoesNotExist:
        if user_course:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.rating = form.cleaned_data['rating']
                data.comment = form.cleaned_data['comment']
                data.ip = request.META.get('REMOTE_ADDR')
                data.course = course
                data.user_id = request.user.id
                data.save()                
                messages.success(request, 'Thank you, your review has been submitted.')
                return redirect(url)
               
        return redirect('checkout', slug)
    
    context = {
        'course_reviews': course_reviews,
        'course_review_list':course_review_list, #I used this to get the count of review in the template
        'nums':nums,
        'average_course_review': average_course_review,
        'review': review,
        'course':course,
        'star_5_percent': str(format(star_5_percent, ".0f"))+'%',
        'star_4_percent': str(format(star_4_percent, ".0f"))+'%',
        'star_3_percent': str(format(star_3_percent, ".0f"))+'%',
        'star_1_percent': str(format(star_1_percent, ".0f"))+'%',
        
    }    
    
    return render(request, template_name="courses/dashboard/student-dashboard/all_review.html", context=context)                 
                
   
   
   
   
   
   

    