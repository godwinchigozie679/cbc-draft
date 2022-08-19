from django.db import models

# Create your models here.

class Social(models.Model):
    pass
    
class SocialHandle(models.Model):
    name = models.CharField(max_length=100)
    username_url = models.CharField(max_length=400,)
    followers_numbers = models.CharField(max_length=100) #use 1k for thousand or 1M for millions
    icon = models.CharField(max_length=150)    
    image = models.ImageField(blank=True, null=True, upload_to='social_handle/social_medial_images', )
    social = models.ForeignKey(Social, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.name}'

class PhoneNumber(models.Model):
    number = models.CharField(max_length=400)
    
    def __str__(self):
        return f'{self.number}'
    
    
class Email(models.Model):
    email = models.EmailField(max_length=254)
    
    
    def __str__(self):
        return f'{self.email}'
    

class OfficeAdress(models.Model):
    address = models.CharField(max_length=400)
    
    def __str__(self):
        return f'{self.address}'