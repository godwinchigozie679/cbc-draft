from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Reverse
from django.urls import reverse
# manage superuser
# manage User
class MyAccountManager(BaseUserManager):
    
    def create_user(self, first_name, last_name, email, username, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')
        
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email), 
            username=username,
            
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_author(self,first_name, last_name, email, username, password,):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.create_user(
            first_name=first_name,            
            last_name=last_name,
            email=self.normalize_email(email), 
            username=username,
            password=password,
        )
        
        user.is_admin = False
        user.is_staff = False
        user.is_author = True
        user.is_superuser = False
        user.save(using=self._db)
        return user
    
   
    def create_superuser(self, first_name, last_name, email, username, password, ):
        
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email), 
            username=username,
            password=password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
    

# Create your models here.

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_images():
    return 'cbc/default_profile/logo_1080_1080.png'
  
class Account(AbstractBaseUser):
    first_name              = models.CharField(max_length=40, blank=True)
    last_name               = models.CharField(max_length=40, blank=True)    
    email                   = models.EmailField(verbose_name='email', max_length=60, unique=True)
    profile_image           = models.ImageField(max_length=250, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_images)
    username                = models.CharField(max_length=60, unique=True, blank=True, null=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True )
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_author               = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    hide_email              = models.BooleanField(default=True)
    is_email_verified       = models.BooleanField(default=False)
   
    
    objects = MyAccountManager()
    
    # username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'username']
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return f'{self.email}'
    
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    
    def has_module_perms(self, app_label):
        return True
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})

class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')     
    phone = models.CharField(max_length=50, blank=True, null=True)    
    facebook_url = models.CharField(max_length=200, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, blank=True, null=True)
    instagram_url = models.CharField(max_length=200, blank=True, null=True)
    pinterest_url = models.CharField(max_length=200, blank=True, null=True)
    # bio = models.TextField(max_length=1000, blank=True, null=True)
    biography = models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user}'
    

    def get_absolute_url(self):      
        return reverse('edit_profile', kwargs={'pk': self.pk})
    
    

class AuthorBankAccount(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='bank_account')     
    bank_name = models.CharField(max_length=50, blank=True, null=True)    
    account_name = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.user}'
    

    def get_absolute_url(self):      
        return reverse('edit_bank_account', kwargs={'pk': self.pk})