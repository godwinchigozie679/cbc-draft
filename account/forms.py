from django import forms
from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import authenticate
from account.models import Account, Profile

# CKEDITOR
from ckeditor.widgets import CKEditorWidget


class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=255, help_text="Required. Add a valied email address.")
    username = forms.CharField(max_length=255, help_text="Required. Add a valied username address.")
    
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)
        
                   
        def cleaned_email(self):
            email = self.cleaned_data['email'].lower()
            
            
            try:
                account = Account.objects.get(email=email)
            except Exception as e:
                return email
            raise forms.ValidationError(f'Email {email} is already in use.')
        
        def cleaned_username(self):
            username = self.cleaned_data['username'].lower()
            
            
            try:
                account = Account.objects.get(username=username)
            except Exception as e:
                return username
            raise forms.ValidationError(f'Username {username} is already in use.')
       




class AccountAuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control my-2 content-comment','placeholder': 'Enter Your Email'}))    
    password = forms.CharField(label = "password", widget= forms.PasswordInput(attrs={'class': 'form-control my-2 content-comment','placeholder': 'Enter Your Password'}))
    
    class Meta:
        model = Account
        fields = ('email', 'password')        
        


# EditProfileAccountForm
class EditProfileAccountForm(ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-2 content-comment','placeholder': 'Enter Your First Name'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-2 content-comment','placeholder': 'Enter Your Last Name'}))
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-2 content-comment','placeholder': 'Enter Your username'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput())
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'profile_image', 'username' ]
       


# EditProfileAccountForm
class EditProfileForm(ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-2 content-comment','placeholder': 'Enter Your Phone Number'}))
    twitter_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-3 content-comment','placeholder': 'Enter Your Twitter url'}))
    facebook_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-3 content-comment','placeholder': 'Enter Your Facebook url'}))
    instagram_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control my-3 content-comment','placeholder': 'Enter Your Instagram url'}))
    biography = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control content-comment my-2','placeholder': 'Your Comment:', "rows":8, "cols":30}))
    
    class Meta:    
        model = Profile
        fields = ['phone', 'twitter_url', 'facebook_url', 'instagram_url', 'biography']
        

        