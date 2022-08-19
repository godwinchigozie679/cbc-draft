from django.db import models
from e_learning.models.course import Course
from e_learning.models.user_course import UserCourse
from account.models import Account
from django.template.defaultfilters import slugify
from e_learning.models.course_modules import Modulee
from e_learning.models.sector import Sector


# Create your models here.
class Video(models.Model):
    title = models.CharField(null=False, max_length=100)
    slug = models.SlugField(null=True, blank=True)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE, related_name='video_course')
    # sector = models.ManyToManyField(Sector, blank=True, null=True)
    # user_course = models.ForeignKey(UserCourse, null=False, on_delete=models.CASCADE, blank=True)
    course_module = models.ForeignKey(Modulee, null=False, on_delete=models.CASCADE, related_name='modules')
    serial_number = models.IntegerField(null=False,)
    video_id = models.CharField(null=False, max_length=200)
    is_preview = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['serial_number', 'course', 'course_module']
    
    def __str__(self):
        return f'{self.course}|>>|....{self.course_module}|>>|....{self.title}'
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    