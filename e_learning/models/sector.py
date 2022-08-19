from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse



# Create your models here.
class Sector(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(blank=True)
    sector_number = models.IntegerField(unique=True,)    
    sector_image=models.ImageField(upload_to='courses/sector_images')
    
    class Meta:
        ordering = ['sector_number']
    
    
    def get_absolute_url(self):
        return reverse("category_course", kwargs={'slug': self.slug}) 
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}'
        
    
    
class SubSector(models.Model):    
    name = models.CharField(blank=True, max_length=200)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='sector')
    slug = models.CharField(max_length=200, blank=True)  
    
    # def get_absolute_url(self):
    #     return reverse("sub_category", kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.sector}>>{self.name}'    