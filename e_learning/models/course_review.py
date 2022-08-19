from django.db import models
from e_learning.models.course import Course
from src import settings
from account.models import Account
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse




# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    subject = models.CharField(max_length=100, blank=True)
    comment = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(default=0.5)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.course}'
    
    def get_absolute_url(self):
        return reverse("submit_review", args=[str(self.course.slug)])
    
    
    class Meta:
        ordering = ['updated_at']

