from django.db import models
from src import settings
from account.models import Profile
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey


# Blog.
class Category(models.Model):    
    name = models.CharField(max_length=200)
    catching_phrase = models.CharField(max_length=100)
    blog_cat_slug = models.CharField(max_length=200, blank=True)    
    category_image = models.ImageField(upload_to='blog_category/category_images')
    
    
    def get_absolute_url(self):
        return reverse("blog_category", kwargs={'blog_cat_slug': self.blog_cat_slug})
    
    def save(self, *args, **kwargs):
        self.blog_cat_slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}'
    
class SubCategory(models.Model):    
    name = models.CharField(blank=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_category' )
    blog_subcat_slug = models.CharField(max_length=200, blank=True)  
    
    # def get_absolute_url(self):
    #     return reverse("blog_category", kwargs={'blog_cat_slug': self.blog_cat_slug})
    
    def save(self, *args, **kwargs):
        self.blog_subcat_slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.category}>>{self.name}'


class BlogPublishedManager(models.Manager):
    def get_queryset(self):
        return super(BlogPublishedManager, self).get_queryset().filter(status='published')



STATUS = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('suspended', 'Suspended'),
)


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    blog_post_slug = models.CharField(max_length=200, unique_for_date='created_on', blank=True)
    post_image = models.ImageField(upload_to='blog/post_images',)       
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='blog_author')    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category',)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='post_subcategory',)    
    content = RichTextField(blank=True)
    overview = models.TextField(max_length=300,)
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15,choices=STATUS, default='draft')
    views = models.IntegerField(default=0,)
    objects = models.Manager()
    blog_published = BlogPublishedManager()
    tags = TaggableManager()
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True)
    
    @property
    def num_liked(self):
        return self.liked.all().count()
    
    def get_absolute_url(self):
        return reverse("blog_post_details", kwargs={'blog_post_slug': self.blog_post_slug})
    
    def save(self, *args, **kwargs):
        self.blog_post_slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return f'{self.title}>>{self.author}' 
        
    
    
    
    
    
# News

# Category
class NewsCategory(models.Model):
    name = models.CharField(max_length=200)
    catching_phrase = models.CharField(max_length=100)
    news_cat_slug = models.CharField(max_length=200, blank=True)
    category_image = models.ImageField(upload_to='news_category/category_images')       
    
    def get_absolute_url(self):
        return reverse("news_category", kwargs={'news_cat_slug': self.news_cat_slug})
    
    def __str__(self):
        return f'{self.name}'
    
    
    def save(self, *args, **kwargs):
        self.news_cat_slug = slugify(self.name)
        super().save(*args, **kwargs)

class NewsSubCategory(models.Model):    
    name = models.CharField(blank=True, max_length=200)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news_category_name')
    news_subcat_slug = models.CharField(max_length=200, blank=True)  
    
    # def get_absolute_url(self):
    #     return reverse("blog_category", kwargs={'blog_cat_slug': self.blog_cat_slug})  
    
    def save(self, *args, **kwargs):
        self.news_subcat_slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.category}>>{self.name}'

class NewsPublishedManager(models.Manager):
    def get_queryset(self):
        return super(NewsPublishedManager, self).get_queryset().filter(status='published')
    
class NewsPost(models.Model):
    title = models.CharField(max_length=200, blank=True)
    news_post_slug = models.CharField(max_length=200, unique_for_date='created_on', blank=True)
    post_image = models.ImageField(upload_to='News/post_images',)    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='news_author')    
    content = RichTextField(blank=True)
    overview = models.TextField(max_length=300,)
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15,choices=STATUS, default='draft')
    views = models.IntegerField(default=0,)
    objects = models.Manager()
    news_published = NewsPublishedManager()    
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news_category',)
    sub_category = models.ForeignKey(NewsSubCategory, on_delete=models.CASCADE, related_name='news_subcategory',)
    tags = TaggableManager()
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True)
    
    @property
    def num_liked(self):
        return self.liked.all().count()
    
    
    def get_absolute_url(self):
        return reverse("news_post_details", kwargs={'news_post_slug': self.news_post_slug})
    
    def save(self, *args, **kwargs):
        self.news_post_slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return f'{self.title}>>{self.author}'     

    
# Comment System
# Blog
class BlogComment(MPTTModel):
    blog_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blog_post_comment',)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='comment_author') 
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    content = models.TextField(max_length=500,)    
    publish = models.DateTimeField(auto_now_add=True,)
    status = models.BooleanField(default=True,)
    
    class MPTTMeta:        
        order_insertion_by = [ '-parent', '-publish',]
        
        
    def __str__(self):
        return f'Comment by {self.author}' 


#News Comment 
class NewsComment(MPTTModel):
    news_post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='news_post_comment',)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='news_comment_author') 
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='news_children')
    content = models.TextField(max_length=500,)
    publish = models.DateTimeField(auto_now_add=True,)
    status = models.BooleanField(default=True,)
    
    
    
    class Meta:
        ordering = ('-publish',)
        
        
    def __str__(self):
        return f'Comment by {self.author}'
    
    


class Advert(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(blank=True, upload_to='Advert/advert_images')
    url = models.URLField()
    
    def __str__(self):
        return f'{self.name}'
    