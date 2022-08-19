from django.db import models
from django.template.defaultfilters import slugify
from e_learning.models.course import Course


# Create your models here.
class Modulee(models.Model):       
    name = models.CharField(null=False, max_length=100)
    slug = models.SlugField(null=True, blank=True)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE, related_name='course_modules') 
    module_number = models.IntegerField()  
    module_quiz_pass_mark = models.FloatField(default=0)             
    
    
    class Meta:
        ordering = ['course', 'module_number']
    

    def __str__(self):
        return f'{self.name}|>>|....{self.course}'
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    