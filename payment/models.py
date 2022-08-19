from django.db import models
from account.models import Account
from e_learning.models.course import Course
from e_learning.models.user_course import UserCourse, AuthorCourse
from e_learning.models.video import Video
import secrets



# Payment Models
class Payment(models.Model):    
    order_id= models.CharField(max_length=200, null=False)
    amount = models.PositiveIntegerField()
    payment_id= models.CharField(max_length=200)
    user_course = models.ForeignKey(UserCourse, null=True, blank=True, on_delete=models.CASCADE)   
    author_course = models.CharField(max_length=200)  
    verified= models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)    
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date_created"]
        
    def __str__(self):
        return f"Payment: {self.user}, Verified: {self.verified}, Course: {self.course}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.order_id:
            order_id = secrets.token_urlsafe(20)
            object_with_similar_order_id = Payment.objects.filter(order_id=order_id)
            if not object_with_similar_order_id:
                self.order_id = order_id
        super().save(*args, **kwargs)
        
        
        
class PaymentExchangeRate(models.Model):
    exchange_rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f'{self.exchange_rate}'
    
      
    
   
    