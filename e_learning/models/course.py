from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from e_learning.models.sector import Sector, SubSector
from src import settings
from django.urls import reverse
from taggit.managers import TaggableManager





# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=200)
  
    
    def __str__(self):
        return f'{self.name}'


class Course(models.Model):
    name = models.CharField(max_length= 200, null=False)   
    slug = models.SlugField(max_length= 200, null=True, blank=True)   
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,related_name='course_category' )
    sub_sector = models.ForeignKey(SubSector, on_delete=models.CASCADE,related_name='sub_category' )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='author_course')
    meta_title = models.TextField(max_length=400)
    description = RichTextUploadingField(max_length=3000)
    price = models.IntegerField(default=0)
    percentage_discount = models.IntegerField(default=0)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,related_name='course_level' )
    active = models.BooleanField(default=False)
    course_completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    certifications = models.TextField(max_length=800)
    thumbnail = models.ImageField(upload_to='courses/thumbnails')
    resources = models.ImageField(upload_to='courses/resources')
    length = models.CharField(help_text='put in weeks example; 12 Weeks', max_length=200)
    views = models.IntegerField(default=0)
    tags = TaggableManager()
    
    
    
    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("main_course", kwargs={'slug': self.slug})
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Prerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requirement') 
    list_items = models.CharField(max_length=200)

class Learning(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='learning')
    list_items = models.CharField(max_length=200)


