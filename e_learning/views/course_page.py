from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from e_learning.models.course_review import Review
from e_learning.models.course import Course, Level
from e_learning.models.sector import Sector, SubSector
from django.views.generic import ListView
from django.template.loader import render_to_string
from src import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




# Create your views here.

class CoursePage(ListView):    
    template_name = "courses/course_page.html"
    
    paginate_by = 9
    
    def get_queryset(self):
        return Course.objects.filter(active=True) 
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["sectors"] = Sector.objects.all()
        context["sub_sectors"] = SubSector.objects.all()
        context["levels"] = Level.objects.all()
        
        courses = Course.objects.filter(active=True,)
        for uncheck in courses:
            context["uncheck"] = uncheck
        
        context["Beginner"] = 'Beginner'
        
        
        context["free"] = Course.objects.filter(active=True, price='0')
        for fe in context["free"]:
            context["fre"] = fe
        
            
        context["paid"] = Course.objects.filter(active=True, price__gte='1') 
        for pay in context["paid"]:
            context["pay"] = pay     
        
                
        return context
    
# Filter

class CoursePageFilter(ListView):
    
    template_name = 'filter/filter-course-page.html'    
    
    
    
    def get(self, request):
        categories = request.GET.getlist('sector[]', None)
        levels = request.GET.getlist('level[]', None)
        free = request.GET.getlist('free[]', None)
        paid = request.GET.getlist('paid[]', None)
        uncheck = request.GET.getlist('uncheck[]', None)
        sub_sectors = request.GET.getlist('subsector[]', None)
        
        courses = Course.objects.filter(active=True,)
        # page = request.GET.get('page')
        # paginator = Paginator(courses, 1)
        # page = request.GET.get('page')
        
        # try:
        #     courses = paginator.page(page)
        # except PageNotAnInteger:
        #     courses = paginator.page(2)
        # except EmptyPage:
        #     courses = paginator.page(paginator.num_pages)
        
        if categories:
            courses = Course.objects.filter(active=True, sector__id__in=categories).distinct().order_by('id')
            # paginator = Paginator(courses, 1)
            # page = request.GET.get('page')
            
            # try:
            #     courses = paginator.page(page)
            # except PageNotAnInteger:
            #     courses = paginator.page(2)
            # except EmptyPage:
            #     courses = paginator.page(paginator.num_pages)
        
        # I used this in the course category filter    
        elif sub_sectors: 
            courses = Course.objects.filter(active=True, sub_sector__id__in=sub_sectors).distinct().order_by('id')
            
        elif levels:
            courses = Course.objects.filter(active=True, level__id__in=levels).distinct().order_by('id')
        elif free:
            courses = Course.objects.filter(active=True, price='0').distinct().order_by('id')
        elif paid:
            courses = Course.objects.filter(active=True, price__gte='1').order_by('id')
        elif uncheck:
            courses = Course.objects.filter(active=True,) 
            
        user = request.user
        context = {
            'courses': courses, 
            # 'page': page,
            'user':user
        }
        
        t = render_to_string(template_name=self.template_name, context=context)    
    
        return JsonResponse({'courses':t})
        
        
        # return render(request, self.template_name, context)
    
    

        
        
        
        
       
