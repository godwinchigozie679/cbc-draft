from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import HttpResponseRedirect
from blog.models import Post, Category, SubCategory, NewsPost, NewsCategory, Advert
from taggit.models import Tag
from django.db.models import Count
from e_learning.models.course import Course
from e_learning.models.course import Sector
from e_learning.models.video import Video
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
# from social_handle.models import SocialHandle
import datetime
# Create your views here.
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
# import forms from form
from blog.models import BlogComment, NewsComment
from blog.form import AddBlogCommentForm, AddNewsCommentForm, BlogCreationForm
# Settions
from src import settings
# Author
from account.models import Account




# Mixin
class BlogNewsTagsMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_tags'] = Post.tags.most_common()# all Tag for Blog
        context['news_common_tags'] = NewsPost.tags.most_common()# all Tag for News
        context['ads'] = Advert.objects.all()# Advert
        context['all_news'] = NewsPost.news_published.all()        
        
        #Post I Use for Guest Post
        context['post'] = Post.blog_published.all()[0]
        
        context['blog_categories'] = Category.objects.all() #blog category
        for post_cat in context['blog_categories'][1:2]:
            context['post_cat_id'] = post_cat.id
        context['post_cat_id'] == 'active'
        
        
        context['news_categories'] = NewsCategory.objects.all() # news_categories
        for cat in context['news_categories'][:1]:
            context['cat_id'] = cat.id
        context['cat_id'] == 'active'
        
        
        return context

class BlogCategoryMixin(object):    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                       
    
        context['blog_post'] = Post.blog_published.filter(category__blog_cat_slug=self.kwargs['blog_cat_slug'])# Post
        for post in context['blog_post']:
            context['category'] = post.category
            
            
        return context
    

class TagSlugMixin(object):    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_post'] = Post.blog_published.filter(tags__slug=self.kwargs['slug'])# Post
        
        for post in context['blog_post']:
            for tag in post.tags.all(): 
                context['tag'] = tag 
               
        return context
    
# Nav Category
class NavCategory(ListView):
            
    
    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])
    
    
    template_name = 'courses/base/blog.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.all()
       
        context["news_categories"] = NewsCategory.objects.all()
        return context



# List View Home #####################################################################

class BlogHome(BlogNewsTagsMixin, ListView):
    
    template_name = 'home.html'
    
    queryset = Post.blog_published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.blog_published.all() #all Post
        
        # More Blog Category for nav
        context["more_blog_categories"] = Category.objects.filter().order_by('?') #all Post
        
        # More News Category
        context['more_news_categories'] = NewsCategory.objects.filter().order_by('?')
        #Post I Use for Guest Post
        context['post'] = Post.blog_published.all()[0]
       
        
        # Popular Post    
        context['all_popular_post'] = Post.blog_published.annotate(Count('views')).order_by('-views')     
        
        # Trending Post
        context['all_trending_post'] = Post.blog_published.annotate(Count('views')).order_by('liked', '-views') 
        
        # Trending News
        context['all_trending_news'] = NewsPost.news_published.annotate(Count('views')).order_by('liked', '-views')     
        
        # Popular News    
        context['popular_news_post'] = NewsPost.news_published.annotate(Count('views')).order_by('-views')
        
        
        # Feature Videos from Course
        context['featured_courses'] = Course.objects.all() 
        context['popular_courses'] = Course.objects.annotate(Count('views')).order_by('-views')
        context['course_categories'] = Sector.objects.filter().order_by('?') 
        
        return context

    
  



""" All Blog Category Details """

class BlogCategoryList(BlogNewsTagsMixin,BlogCategoryMixin, ListView):    
    
    template_name = 'blog/blog_category_post.html'   
      
    paginate_by = settings.pagination_number    
    
    def get_queryset(self):
        return Post.blog_published.filter(category__blog_cat_slug=self.kwargs['blog_cat_slug']) 
             
        

# Blog Category Filter   
class LastestBlogPostCategory(BlogNewsTagsMixin,BlogCategoryMixin, ListView):
    template_name = 'blog/blog_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return Post.blog_published.filter(category__blog_cat_slug=self.kwargs['blog_cat_slug']) 
        
    

class MostReadBlogPostCategory(BlogNewsTagsMixin,BlogCategoryMixin, ListView):
    
    template_name = 'blog/blog_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return Post.blog_published.filter(category__blog_cat_slug=self.kwargs['blog_cat_slug']).annotate(Count('views')).order_by('liked', '-views')# Post
        
         


class MostViewedBlogPostCategory(BlogNewsTagsMixin,BlogCategoryMixin, ListView):
    
    template_name = 'blog/blog_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return Post.blog_published.filter(category__blog_cat_slug=self.kwargs['blog_cat_slug']).annotate(Count('views')).order_by('-views')# Post


class MostCommentedBlogPostCategory(BlogNewsTagsMixin,BlogCategoryMixin, ListView):
    
    template_name = 'blog/blog_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return Post.blog_published.filter(category__blog_cat_slug=self.kwargs['blog_cat_slug']).annotate(Count('blog_post_comment')).order_by('blog_post_comment')# Post
                


""" All Tag Blog Post Details """ 

class BlogTagList(BlogNewsTagsMixin, TagSlugMixin, ListView):
    
    template_name = 'blog/blog_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return Post.blog_published.filter(tags__slug=self.kwargs['slug']) 

""" All Blog Post Details """


# All post filter
class LastestBlogPostList(BlogNewsTagsMixin, ListView):
    queryset = Post.blog_published.all()  
    
    paginate_by = settings.pagination_number    
    
    template_name = 'blog/blog_category_post.html'  


# Most Read   
class MostReadBlogPostList(BlogNewsTagsMixin, ListView):
    
    queryset = Post.blog_published.all().order_by('liked', '-views')# Post  
    
    paginate_by = settings.pagination_number
    
    template_name = 'blog/blog_category_post.html' 
     

# Most Viewed
class MostViewedBlogPostList(BlogNewsTagsMixin, ListView):
    
    queryset = Post.blog_published.all().annotate(Count('views')).order_by('-views')# Post 
    
    paginate_by = settings.pagination_number  
    
    template_name = 'blog/blog_category_post.html' 


# Most Commented
class MostCommentedBlogPostList(BlogNewsTagsMixin, ListView):
    
    template_name = 'blog/blog_category_post.html'
    
    queryset = Post.blog_published.all().annotate(Count('blog_post_comment')).order_by('blog_post_comment')# Post  
    
    paginate_by = settings.pagination_number
    
     
    

""" Blog Post Detail Views """

class BlogPostDetails(BlogNewsTagsMixin, MultipleObjectMixin, DetailView):    
        
    template_name = 'blog/blog_post.html'
    
    paginate_by = 6
    
    def get_object(self):
        return get_object_or_404(Post, blog_post_slug=self.kwargs['blog_post_slug'])   
    
    def get_context_data(self, **kwargs):
        
        
        object_list = BlogComment.objects.filter(status='True', blog_post=self.get_object()) #comment        
        
        context = super(BlogPostDetails, self).get_context_data(object_list=object_list, **kwargs)
        
        context['post'] = get_object_or_404(Post, blog_post_slug=self.kwargs['blog_post_slug']) #Post
        
        
        for comment in object_list:
            context['comment'] = comment
        
        post_tags =   context['post'].tags.all() 
        related_post = Post.blog_published.filter(status='published', tags__in = post_tags).exclude(blog_post_slug=self.kwargs['blog_post_slug'])#USE TO GET RELATED POST
        
        
        context['related_post'] = related_post.annotate(tag_count=Count('tags')).order_by('-tag_count', '-publish')  #related post list        
        
        context['category'] = context['post'].category #Category
        
        if self.request.user.is_authenticated:
            context['comment_form'] = AddBlogCommentForm(instance=self.request.user)        
              
        return context

    

"""Create Blog Comment"""  
class CreateBlogComment(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'# redirect after successful login
    
    model = BlogComment
    form_class = AddBlogCommentForm   
    template_name = 'blog/blog_post.html'
    
    def get_object(self):
        return get_object_or_404(BlogComment, blog_post__id=self.kwargs['pk'])
    
    def form_valid(self, form):                    
        form.instance.author = self.request.user        
        form.instance.blog_post_id = self.kwargs['pk']
        
        if not form.instance.content:
           return redirect('latest_post')#I will come back
            
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(
            self.request, 'Your comment has been created successfully.')
        
        return reverse('blog_post_details', kwargs={'blog_post_slug': self.object.blog_post.blog_post_slug} )

"""Update Blog Comment"""     
class UpdateBlogComment(LoginRequiredMixin, UpdateView):
    model = BlogComment
    
    template_name = 'blog/blog_post.html'
    
    form_class = AddBlogCommentForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user    
        
        if not form.instance.content:                      
            return redirect('latest_post')#I will come back
            
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(
            self.request, 'Your comment has been updated successfully.')
        
        return reverse('blog_post_details', kwargs={'blog_post_slug': self.object.blog_post.blog_post_slug} )
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

###########################################
#Blog Author Page

class BlogAuthorParameterMixin(object):
    
    template_name = 'blog/blog_author.html'
    
    def get_object(self):
        return get_object_or_404(Account,blog_author__id=self.kwargs['pk'] )    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) 
        
        context['post'] = get_object_or_404(Post, pk= self.kwargs['pk']) #Pos
        
        context['account'] = get_object_or_404(Account,blog_author__id=self.kwargs['pk'] )
        
        context['object_list'] = Post.blog_published.filter(author_id=self.get_object()) #author post
        
        context['post_count'] = context['object_list'].count() #count of post by author
        
        context['total_views'] = context['object_list'].aggregate(total_views=Sum('views'))['total_views'] # Total views
        
        return context
    

class BlogAuthor(BlogNewsTagsMixin, ListView):    
    
    paginate_by = settings.pagination_number
    
    template_name = 'blog/blog_author.html'
    
    def get_object(self):
        return get_object_or_404(Account,blog_author__id=self.kwargs['pk'] )    
    
    def get_queryset(self):
        return Post.blog_published.filter(author_id=self.get_object())
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) 
        
        context['post'] = get_object_or_404(Post, pk= self.kwargs['pk']) #Pos
        
        context['account'] = get_object_or_404(Account,blog_author__id=self.kwargs['pk'] )
        
        context['object_list'] = Post.blog_published.filter(author_id=self.get_object()) #author post
        
        context['post_count'] = context['object_list'].count() #count of post by author
        
        context['total_views'] = context['object_list'].aggregate(total_views=Sum('views'))['total_views'] # Total views
        
        return context

# All Author post filter
class LastestBlogAuthorPostList(BlogNewsTagsMixin, BlogAuthorParameterMixin, ListView):  
    
    def get_queryset(self):
        return Post.blog_published.filter(author_id=self.get_object())    
    
    paginate_by = settings.pagination_number    
    
      


# Most Read   
class MostReadBlogAuthorPostList(BlogNewsTagsMixin, BlogAuthorParameterMixin, ListView):
    
    def get_queryset(self):
        return Post.blog_published.filter(author_id=self.get_object()).order_by('liked', '-views')# Post  
    
    paginate_by = settings.pagination_number
    
    
     

# Most Viewed
class MostViewedBlogAuthorPostList(BlogNewsTagsMixin, BlogAuthorParameterMixin, ListView):
    
    def get_queryset(self):
        return Post.blog_published.filter(author_id=self.get_object()).annotate(Count('views')).order_by('-views')# Post 
    
    paginate_by = settings.pagination_number      


# Most Commented
class MostCommentedBlogAuthorPostList(BlogNewsTagsMixin, BlogAuthorParameterMixin, ListView):    
    
    
    def get_queryset(self):
        return Post.blog_published.filter(author_id=self.get_object()).annotate(Count('blog_post_comment')).order_by('blog_post_comment')# Post  
    
    paginate_by = settings.pagination_number
    
############################################################ # Blog Portal  
# Blog Portal
class BlogPortal(LoginRequiredMixin, ListView):
    
    login_url = '/login/'
    
    redirect_field_name = 'next'# redirect after successful login
    
    paginate_by = settings.pagination_number
    
    template_name = 'blog/blog_portal.html' 
    
    def get_object(self):
        return Account.objects.get(blog_author__id=self.kwargs['pk'])
    
    def get_queryset(self):        
        return Post.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) 
        
        context['user'] = self.request.user
        context['account'] = Account.objects.filter(username=context['user']) #account           
        
        context['object_list'] = Post.objects.filter(author=context['user'],) #author post
        for post in context['object_list']:
            context['post'] = post
        
        context['post_count'] = context['object_list'].count() #count of post by author
        
        context['total_views'] = context['object_list'].aggregate(total_views=Sum('views'))['total_views'] # Total views
        
        return context
    

class BlogPortalParameterMixin(object):
    
    template_name = 'blog/blog_portal.html'
    
    def get_object(self):
        return Account.objects.get(blog_author=self.kwargs['pk'])     
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) 
        
        context['user'] = self.request.user
        context['account'] = Account.objects.filter(username=context['user']) #Post   
        
        context['object_list'] = Post.objects.filter(author=context['user'],) #author post
        for post in context['object_list']:
            context['post'] = post
        
        context['post_count'] = context['object_list'].count() #count of post by author
        
        context['total_views'] = context['object_list'].aggregate(total_views=Sum('views'))['total_views'] # Total views
        
        return context

# All Blog Portal filter
class LastestBlogPortalPostList(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):  
    
    def get_queryset(self):        
        return Post.objects.filter(author=self.request.user)    
    
    paginate_by = settings.pagination_number    
    
      


# Most Read   
class MostReadBlogPortalPostList(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):
    
    def get_queryset(self):        
        return Post.objects.filter(author=self.request.user).order_by('liked', '-views')# Post  
    
    paginate_by = settings.pagination_number   
    
     

# Most Viewed
class MostViewedBlogPortalPostList(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):
    
    def get_queryset(self):        
        return Post.objects.filter(author=self.request.user).annotate(Count('views')).order_by('-views')# Post 
    
    paginate_by = settings.pagination_number      


# Most Commented
class MostCommentedBlogPortalPostList(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):    
    
    
    def get_queryset(self):        
        return Post.objects.filter(author=self.request.user).annotate(Count('blog_post_comment')).order_by('blog_post_comment')# Post  
    
    paginate_by = settings.pagination_number
    
# ######### FIlter blog portal based on published, draft and suspended

# Published    
class MostReadBlogPortalPostPublished(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):
    def get_queryset(self):        
        return Post.objects.filter(status='published', author=self.request.user,)
    
    paginate_by = settings.pagination_number

#Draft   
class MostViewedBlogPortalPostDraft(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):
    def get_queryset(self):        
        return Post.objects.filter(status='draft', author=self.request.user,)
    
    paginate_by = settings.pagination_number

#Suspended 
class MostCommentedBlogPortalPostSuspended(BlogNewsTagsMixin, BlogPortalParameterMixin, ListView):
    def get_queryset(self):        
        return Post.objects.filter(status='suspended', author=self.request.user,)
    
    paginate_by = settings.pagination_number
    
    
############################################## CREATE BLOG POST
class CreateBlogPost(LoginRequiredMixin, CreateView):
    
    login_url = '/login'
    redirect_field_name = 'next'
        
    template_name = 'blog/blog_creation_form.html'
    
    model = Post
    
    form_class = BlogCreationForm
    
    def form_valid(self, form):                    
        form.instance.author = self.request.user 
        
        
        
        
        if not form.instance.content:
           return redirect('create_blog_post')#I will come back
            
        return super().form_valid(form)
    
        if not form.instance.overview:
               return redirect('create_blog_post')#I will come back
        
        if not form.instance.tags:
               return redirect('create_blog_post')#I will come back
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        # post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(
            self.request, 'Your Article has been created successfully.')
        
        return reverse('create_blog_post')    
    
    #Uodate View
class UpdateBlogPost(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'next'
    
    model = Post
    form_class = BlogCreationForm    
    template_name = 'blog/blog_creation_form.html'    
        
    # Post the data into the DB
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        form = BlogCreationForm(request.POST, instance=post)        
        if form.is_valid():
            edit_post = form.save(commit=False)
            form.instance = self.request.user                       
            edit_post.save()
            return redirect('blog_portal', post.pk)
        return render(request,  {'form': form})   
    
############################################################################################

class NewsCategoryMixin(object):    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                       
    
        context['news_post'] = NewsPost.news_published.filter(category__news_cat_slug=self.kwargs['news_cat_slug'])# Post
        for news in context['news_post']:
            context['category'] = news.category
            
        return context
    

class NewsTagSlugMixin(object):    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_post'] = NewsPost.news_published.filter(tags__slug=self.kwargs['slug'])# News
        
        for news in context['news_post']:
            for tag in news.tags.all(): 
                context['tag'] = tag 
               
        return context
    
# News Category Details
class NewsCategoryList(BlogNewsTagsMixin, NewsCategoryMixin, ListView):
    
    template_name = 'news/news_category_post.html'   
    
    paginate_by = settings.pagination_number 
    
    def get_queryset(self):
        return NewsPost.news_published.filter(category__news_cat_slug=self.kwargs['news_cat_slug']) # News
            

# News Category Filter   
class LastestNewsPostCategory(BlogNewsTagsMixin,NewsCategoryMixin, ListView):
    template_name = 'news/news_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return NewsPost.news_published.filter(category__news_cat_slug=self.kwargs['news_cat_slug']) 
        
    

class MostReadNewsPostCategory(BlogNewsTagsMixin,NewsCategoryMixin, ListView):
    
    template_name = 'news/news_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return NewsPost.news_published.filter(category__news_cat_slug=self.kwargs['news_cat_slug']).annotate(Count('views')).order_by('liked', '-views')# Post
 
class MostViewedNewsPostCategory(BlogNewsTagsMixin,NewsCategoryMixin, ListView):
    
    template_name = 'news/news_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return NewsPost.news_published.filter(category__news_cat_slug=self.kwargs['news_cat_slug']).annotate(Count('views')).order_by('-views')# Post


class MostCommentedNewsPostCategory(BlogNewsTagsMixin,NewsCategoryMixin, ListView):
    
    template_name = 'news/news_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return NewsPost.news_published.filter(category__news_cat_slug=self.kwargs['news_cat_slug']).annotate(Count('news_post_comment')).order_by('news_post_comment')# Post


""" All Tag news List Post Details """ 

class NewsTagList(BlogNewsTagsMixin, NewsTagSlugMixin, ListView):
    
    template_name = 'news/news_category_post.html'
    
    paginate_by = settings.pagination_number
    
    def get_queryset(self):
        return NewsPost.news_published.filter(tags__slug=self.kwargs['slug']) 

""" All Blog news List Details """


# All News post list filter
class LastestNewsPostList(BlogNewsTagsMixin, ListView):
    queryset = NewsPost.news_published.all()  
    
    paginate_by = settings.pagination_number    
    
    template_name = 'news/news_category_post.html'  


# Most Read   
class MostReadNewsPostList(BlogNewsTagsMixin, ListView):
    
    queryset = NewsPost.news_published.all().order_by('liked', '-views')# news  
    
    paginate_by = settings.pagination_number    
    
    template_name = 'news/news_category_post.html' 
     

# Most Viewed
class MostViewedNewsPostList(BlogNewsTagsMixin, ListView):
    
    queryset = NewsPost.news_published.all().annotate(Count('views')).order_by('-views')# News 
    
    paginate_by = settings.pagination_number  
    
    template_name = 'news/news_category_post.html' 


# Most Commented
class MostCommentedNewsPostList(BlogNewsTagsMixin, ListView):
    paginate_by = settings.pagination_number
    
    template_name = 'news/news_category_post.html'
    
    queryset = NewsPost.news_published.all().annotate(Count('news_post_comment')).order_by('news_post_comment')# News 
    
    
                 
    

""" News Post Detail Views """

class NewsPostDetails(BlogNewsTagsMixin, MultipleObjectMixin, DetailView):    
        
    template_name = 'news/news_post.html'
    
    paginate_by = 6
    
    def get_object(self):
        return get_object_or_404(NewsPost, news_post_slug=self.kwargs['news_post_slug'])   
    
    def get_context_data(self, **kwargs):
        
        
        object_list = NewsComment.objects.filter(status='True', news_post=self.get_object()) #comment        
        
        context = super(NewsPostDetails, self).get_context_data(object_list=object_list, **kwargs)
        
        context['post'] = get_object_or_404(NewsPost, news_post_slug=self.kwargs['news_post_slug']) #Post
        
        
        for comment in object_list:
            context['comment'] = comment
        
        post_tags =   context['post'].tags.all() 
        related_post = NewsPost.news_published.filter(status='published', tags__in = post_tags).exclude(news_post_slug=self.kwargs['news_post_slug'])#USE TO GET RELATED POST
        
        
        context['related_post'] = related_post.annotate(tag_count=Count('tags')).order_by('-tag_count', '-publish')  #related post list        
        
        context['category'] = context['post'].category #Category
        
        if self.request.user.is_authenticated:
            context['comment_form'] = AddNewsCommentForm(instance=self.request.user)        
              
        return context
    
    
    
"""Create News Comment"""  
class CreateNewsComment(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'# redirect after successful login
    
    model = NewsComment
    form_class = AddNewsCommentForm   
    template_name = 'news/news_post.html'
    
    def get_object(self):
        return get_object_or_404(NewsComment, news_post__id=self.kwargs['pk'])
    
    def form_valid(self, form):                    
        form.instance.author = self.request.user        
        form.instance.news_post_id = self.kwargs['pk']
        
        if not form.instance.content:
           return redirect('latest_news')#I will come back
            
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(
            self.request, 'Your comment has been created successfully.')
        
        return reverse('news_post_details', kwargs={'news_post_slug': self.object.news_post.news_post_slug} )

"""Update News Comment"""     
class UpdateNewsComment(LoginRequiredMixin, UpdateView):
    model = NewsComment
    
    template_name = 'news/news_post.html'
    
    form_class = AddNewsCommentForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user    
        
        if not form.instance.content:                      
            return redirect('latest_news')#I will come back
            
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(
            self.request, 'Your comment has been updated successfully.')
        
        return reverse('news_post_details', kwargs={'news_post_slug': self.object.news_post.news_post_slug} )
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

###########################################
#News Author Page

class NewsAuthorParameterMixin(object):
    
    template_name = 'news/news_author.html'
    
    def get_object(self):
        return get_object_or_404(Account,news_author__id=self.kwargs['pk'] )    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) 
        
        context['post'] = get_object_or_404(Post, pk= self.kwargs['pk']) #Pos
        
        context['account'] = get_object_or_404(Account,news_author__id=self.kwargs['pk'] )
        
        context['object_list'] = NewsPost.news_published.filter(author_id=self.get_object()) #author post
        
        context['post_count'] = context['object_list'].count() #count of post by author
        
        context['total_views'] = context['object_list'].aggregate(total_views=Sum('views'))['total_views'] # Total views
        
        return context
    

class NewsAuthor(BlogNewsTagsMixin, ListView):    
    
    paginate_by = settings.pagination_number
    
    template_name = 'news/news_author.html'
    
    def get_object(self):
        return get_object_or_404(Account,news_author__id=self.kwargs['pk'] )    
    
    def get_queryset(self):
        return NewsPost.news_published.filter(author_id=self.get_object())
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) 
        
        context['post'] = get_object_or_404(Post, pk= self.kwargs['pk']) #Pos
        
        context['account'] = get_object_or_404(Account,news_author__id=self.kwargs['pk'] )
        
        context['object_list'] = NewsPost.news_published.filter(author_id=self.get_object()) #author post
        
        context['post_count'] = context['object_list'].count() #count of post by author
        
        context['total_views'] = context['object_list'].aggregate(total_views=Sum('views'))['total_views'] # Total views
        
        return context

# All Author post filter
class LastestNewsAuthorPostList(BlogNewsTagsMixin, NewsAuthorParameterMixin, ListView):  
    
    def get_queryset(self):
        return NewsPost.news_published.filter(author_id=self.get_object())    
    
    paginate_by = settings.pagination_number    
    
      


# Most Read   
class MostReadNewsAuthorPostList(BlogNewsTagsMixin, NewsAuthorParameterMixin, ListView):
    
    def get_queryset(self):
        return NewsPost.news_published.filter(author_id=self.get_object()).order_by('liked', '-views')# Post  
    
    paginate_by = settings.pagination_number
    
    
     

# Most Viewed
class MostViewedNewsAuthorPostList(BlogNewsTagsMixin, NewsAuthorParameterMixin, ListView):
    
    def get_queryset(self):
        return NewsPost.news_published.filter(author_id=self.get_object()).annotate(Count('views')).order_by('-views')# Post 
    
    paginate_by = settings.pagination_number  
    
    


# Most Commented
class MostCommentedNewsAuthorPostList(BlogNewsTagsMixin, NewsAuthorParameterMixin, ListView):    
    
    
    def get_queryset(self):
        return NewsPost.news_published.filter(author_id=self.get_object()).annotate(Count('news_post_comment')).order_by('news_post_comment')# Post  
    
    paginate_by = settings.pagination_number