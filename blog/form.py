from django import forms
from blog.models import BlogComment, NewsComment, Post, NewsPost
from mptt.forms import TreeNodeChoiceField
from django.forms.widgets import FileInput
# CKEDITOR
from ckeditor.widgets import CKEditorWidget
# Taggit
from taggit.forms import *







"""blog_comment form"""

class AddBlogCommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control content-comment','placeholder': 'Your Comment:', "rows":5, "cols":20}))
    parent = TreeNodeChoiceField(queryset=BlogComment.objects.all(),widget=forms.HiddenInput() )    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        
        # content 
        self.fields['content'].label = '' 
        self.fields['content'].required = False       
         
    class Meta:    
        model = BlogComment
        fields =('parent', 'content', )



"""news_comment form"""

class AddNewsCommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control content-comment','placeholder': 'Your Comment:', "rows":5, "cols":20}))
    parent = TreeNodeChoiceField(queryset=NewsComment.objects.all(),widget=forms.HiddenInput() )    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        
        # content 
        self.fields['content'].label = '' 
        self.fields['content'].required = False       
         
    class Meta:    
        model = NewsComment
        fields =('parent', 'content', )
        

"""Blog Creation Form"""
class BlogCreationForm(forms.ModelForm):    
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control content-comment my-2','placeholder': 'Write your Title'}))    
    post_image = forms.ImageField(required=True, widget=forms.FileInput())     
    content = forms.CharField(required=False, widget=CKEditorWidget(attrs={'class': 'form-control content-comment my-2','placeholder': 'Write your Article:',}))
    overview = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control content-comment my-2','placeholder': 'Write your Article Overview: (Maximum words = "300")', "rows":5, "cols":20}))
    tags = TagField(required=False, widget=TagWidget(attrs={'class': 'form-control content-comment my-2','placeholder': 'enter your tags seperated with comma (e.g; crypto, digital,)', "rows":5, "cols":20}))
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
    #     self.fields['parent'].widget.attrs.update(
    #         {'class': 'd-none'})
    #     self.fields['category'].label = ''
    #     self.fields['parent'].required = False
        
    #     # Image Title Change         
        self.fields['category'].option = 'Select Category'
     
  
         
    class Meta:    
        model = Post
        fields = ('title','category', 'sub_category', 'post_image', 'content', 'overview', 'tags'  )
        
        widgets = {
        'category': forms.Select(attrs={'class': 'form-control content-comment my-2',}),
        'sub_category': forms.Select(attrs={'class': 'form-control content-comment my-2',}),
        
        }
       