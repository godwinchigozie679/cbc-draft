from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class SiteReview(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(blank=True)
    career_title = models.CharField(max_length=225)
    ratings = models.FloatField(default=0.0) 
    comment = models.TextField(max_length=500) 
    image=models.ImageField(upload_to='courses/site_review')
    
    class Meta:
        ordering = ['ratings']
    
    
    # def get_absolute_url(self):
    #     return reverse("category_course", kwargs={'slug': self.slug}) 
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}'



class VideoReview(models.Model):
    name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=250)
    image= models.ImageField(upload_to='courses/video_review')
    
    # class Meta:
    #         verbose_name = ''
    
    def __str__(self):
        return f'{self.name}'
    


class Partners(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='courses/site_partners')
    
    class Meta:
            verbose_name = 'Partner'
    
    def __str__(self):
        return f'{self.name}'