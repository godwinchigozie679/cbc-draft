from django.db import models
from e_learning.models.course import Course
       

class AuthorCommision(models.Model):
    percentage = models.IntegerField()
    # course = foreign_key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f'{self.percentage}'
    
      
    
   
    