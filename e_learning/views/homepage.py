from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from e_learning.models.course import Course
from e_learning.models.sector import Sector
from e_learning.models.video import Video
from e_learning.models.user_course import UserCourse
from e_learning.models.course_review import Review
from django.views.generic import ListView
from django.template.loader import render_to_string
from metafeatures.models import SiteReview, VideoReview, Partners
from blog.models import Post

class HOME(ListView):
    
    template_name = "courses/home.html"  
    
    queryset = Course.objects.filter(active=True)   
    
    
    context_object_name = 'courses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        vidio_review = VideoReview.objects.all() #video review
        for v in vidio_review:
            context['video_review'] = v
        
        
        context['site_review'] = SiteReview.objects.all() #site review
        
        context['partners'] = Partners.objects.all() #Partners
        
        # Popular Post    
        context['all_popular_post'] = Post.blog_published.annotate(Count('views')).order_by('-views')
        
        # Most Popular Course
        context['popular_courses'] = Course.objects.annotate(Count('views')).order_by('-views')
        tag_data = []  
        for course in context['popular_courses']:
            for tag in course.tags.all():
                tag_data.append(tag)
        context['popular_course_'] = tag_data
        
        
        courses = Course.objects.filter(active=True)      
        
        alls = Course.objects.filter(active=True)  
          
        for all in alls:            
            context["all"] = all            
            
            
        trendings = Course.objects.filter(active=True).annotate(Count('views')).order_by('-views')
        for trending in trendings:            
            context["trending"] = trending
           
            
        popularities = Course.objects.filter(active=True).annotate(Count('reviews')).order_by('views', '-reviews')
        for popularity in popularities:            
            context["popularity"] = popularity
            
        features = Course.objects.filter(active=True).annotate(Count('level')).order_by('level')
        for featured in features:            
            context["featured"] = featured
        
        context['categories'] = Sector.objects.all()
        
        categories = Course.objects.filter(active=True,).annotate(Count('sector')).order_by('sector')
        for category in categories:            
            context["category"] = category
        
        
        return context
    


def home_filter_data(request):
    
    all = request.GET.getlist('all[]')
    trendings = request.GET.getlist('trending[]')
    popularities = request.GET.getlist('popularity[]')   
    features = request.GET.getlist('featured[]')
    categories = request.GET.getlist('category[]')
    user = request.user
    
    
    courses = Course.objects.filter(active=True).order_by('-id')
    
    if all:
        courses = Course.objects.filter(active=True).distinct()
    if trendings:
        courses = Course.objects.filter(active=True).annotate(Count('views')).order_by('-views').distinct()
    if popularities:
        courses = Course.objects.filter(active=True).annotate(Count('reviews')).order_by('views', '-reviews').distinct()
    if features:
        courses = Course.objects.filter(active=True).annotate(Count('level')).order_by('level').distinct()
    if categories:
        courses = Course.objects.filter(active=True,).annotate(Count('sector')).order_by('sector').distinct()
     
    
    t = render_to_string(template_name='filter/filtered-courses.html', context={'courses': courses, 'user':user})    
    
    return JsonResponse({'courses':t})