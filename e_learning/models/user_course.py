from django.db import models
from account.models import Account
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from django.urls import reverse

# Create Course User models
class UserCourse(models.Model):    
    user = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE, related_name='enroll_students')
    date = models.DateTimeField(auto_now_add=True)
    
    
    def get_absolute_url(self):
        return reverse("user_course", args=[str(self.course.slug)])
    
    def __str__(self):
        return f'Course: {self.course}'


class UserModule(models.Model):
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, related_name='user_course')
    user_course_module = models.ForeignKey(Modulee, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'Course: {self.user_course}'
    




#MMMMMMMMMMMMMMMMMMMMMMMM
class AuthorCourse(models.Model):    
    user = models.ForeignKey(Account, on_delete=models.CASCADE,)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return f'Course: {self.course}'