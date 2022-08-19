from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from e_learning.models.course import Course, Level
from e_learning.models.sector import Sector, SubSector
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from src import settings
# IMPORT PIGINATOR

from django.core.paginator import Paginator

class CategoryCourse(ListView):
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return Course.objects.filter(sector__slug=self.kwargs['slug'])
    
    
    template_name = "courses/course_category.html"   
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["courses"] = Course.objects.filter(sector__slug=self.kwargs['slug'])
        context["sectors"] = Sector.objects.all().exclude(slug=self.kwargs['slug']) 
        context["sector_"] = context["sectors"][0]     
        context["sub_sectors"] = SubSector.objects.filter(sector__slug=self.kwargs['slug'])
        
        context["free"] = Course.objects.filter(price='0', sector__slug=self.kwargs['slug'])
        for fe in context["free"]:
            context["fre"] = fe
            
        context["paid"] = Course.objects.filter(price__gte='1', sector__slug=self.kwargs['slug'])
        for pay in context["paid"]:
            context["pay"] = pay
        
        context["levels"] = Level.objects.all()
        
               
        
        return context
    
    
# Filter

class CourseCategoryFilter(ListView):
    
    template_name = 'filter/filter-course-page.html'
    
    def get(self, request):
        slug = request.GET.get('slug[]', None)               
        levels = request.GET.getlist('level[]', None)
        free = request.GET.getlist('free[]', None)
        paid = request.GET.getlist('paid[]', None)
        uncheck = request.GET.getlist('uncheck[]', None)
        sub_sectors = request.GET.getlist('subsector[]', None)
        
        
        courses = Course.objects.filter(active=True, sector__slug=slug)  
         
        
        # I used this in the course category filter    
        if sub_sectors: 
            courses = Course.objects.filter(active=True, sector__slug=slug, sub_sector__id__in=sub_sectors).distinct().order_by('id')
          
        elif levels:
            courses = Course.objects.filter(active=True, sector__slug=slug, level__id__in=levels).distinct().order_by('id')
        elif free:
            courses = Course.objects.filter(active=True, sector__slug=slug, price='0').distinct().order_by('id')
        elif paid:
            courses = Course.objects.filter(active=True, sector__slug=slug, price__gte='1').order_by('id')
        elif uncheck:
            courses = Course.objects.filter(active=True, sector__slug=slug) 
            
        user = request.user
        context = {
            'courses': courses, 
            # 'page': page,
            'user':user
        }
        
        t = render_to_string(template_name=self.template_name, context=context)    
    
        return JsonResponse({'courses':t})
        
       