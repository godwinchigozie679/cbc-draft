from django.urls import path
from blog import views


urlpatterns = [    
    # Nav Category
    path('blog/category', views.NavCategory.as_view(), name='nav_category'),  
    
    # Home
    # path('blog/category', all_post, name='all_post'),
    path('blog/', views.BlogHome.as_view(), name='blog_home'), 
    
    # Blog
    # blog_category_List_details
    path('blog/<str:blog_cat_slug>/category', views.BlogCategoryList.as_view(), name='blog_category'),    
    # All Blog Post Category List Filter
    path('blog/<str:blog_cat_slug>/latest', views.LastestBlogPostCategory.as_view(), name='latest_blog_category'),
    path('blog/<str:blog_cat_slug>/most_read', views.MostReadBlogPostCategory.as_view(), name='most_read_blog_category'),
    path('blog/<str:blog_cat_slug>/most_viewd', views.MostViewedBlogPostCategory.as_view(), name='most_viewed_blog_category'),
    path('blog/<str:blog_cat_slug>/most_commented', views.MostCommentedBlogPostCategory.as_view(), name='most_commented_blog_category'),
    
    # Tag
    # Tag List Details
    path('blog/<str:slug>/tag', views.BlogTagList.as_view(), name='blog_tag_list'),
    
    
    # All Blog Post List Filter
    path('latest/post', views.LastestBlogPostList.as_view(), name='latest_post'),
    path('most-read/post', views.MostReadBlogPostList.as_view(), name='most_read'),
    path('most-viewed/post', views.MostViewedBlogPostList.as_view(), name='most_viewed'),
    path('most-commented/post', views.MostCommentedBlogPostList.as_view(), name='most_commented'),
    
    # blog_post_details 
    path('blog/<str:blog_post_slug>/post', views.BlogPostDetails.as_view(), name='blog_post_details'),
    
    # blog comment post
    path('blog/<int:pk>/post_comment', views.CreateBlogComment.as_view(), name='add_blog_post_comment'),
    path('blog/<int:pk>/update_comment', views.UpdateBlogComment.as_view(), name='update_blog_post_comment'),
    
    #Blog Author
    path('blog/<int:pk>/author', views.BlogAuthor.as_view(), name='blog_author'),
    # All Blog Author Post List Filter
    path('latest/blog/<int:pk>/post', views.LastestBlogAuthorPostList.as_view(), name='latest_post_author_post'),
    path('most-read/blog/<int:pk>/post', views.MostReadBlogAuthorPostList.as_view(), name='most_read_author_post'),
    path('most-viewed/blog/<int:pk>/post', views.MostViewedBlogAuthorPostList.as_view(), name='most_viewed_author_post'),
    path('most-commented/blog/<int:pk>/post', views.MostCommentedBlogAuthorPostList.as_view(), name='most_commented_author_post'),
   
   
    # blog_portal
    path('blog/blog_portal/<int:pk>/blog_portal', views.BlogPortal.as_view(), name='blog_portal'),
    # All Blog Author Post List Filter
    path('latest/blog/<int:pk>/blog_portal', views.LastestBlogPortalPostList.as_view(), name='latest_post_blog_portal'),
    path('most-read/blog/<int:pk>/blog_portal', views.MostReadBlogPortalPostList.as_view(), name='most_read_post_portal'),
    path('most-viewed/blog/<int:pk>/blog_portal', views.MostViewedBlogPortalPostList.as_view(), name='most_viewed_post_portal'),
    path('most-commented/blog/<int:pk>/blog_portal', views.MostCommentedBlogPortalPostList.as_view(), name='most_commented_post_portal'),
            #published, draft, suspended
    path('most-read/blog/<int:pk>/blog_published', views.MostReadBlogPortalPostPublished.as_view(), name='blog_published'),
    path('most-viewed/blog/<int:pk>/blog_draft', views.MostViewedBlogPortalPostDraft.as_view(), name='blog_draft'),
    path('most-commented/blog/<int:pk>/blog_suspended', views.MostCommentedBlogPortalPostSuspended.as_view(), name='blog_suspended'),
    
    
    
    # Create Post
    path('blog_post/blog/create-blog_post', views.CreateBlogPost.as_view(), name='create_blog_post'),
     path('blog_post/blog/<int:pk>/update-blog_post', views.UpdateBlogPost.as_view(), name='update_blog_post'),
    ##################################################################################################
      
           
    # News
    # news_category_list_details 
    path('news/<str:news_cat_slug>/category', views.NewsCategoryList.as_view(), name='news_category'),     
    # All News Post Category List Filter
    path('news/<str:news_cat_slug>/latest', views.LastestNewsPostCategory.as_view(), name='latest_news_category'),
    path('news/<str:news_cat_slug>/most_read', views.MostReadNewsPostCategory.as_view(), name='most_read_news_category'),
    path('news/<str:news_cat_slug>/most_viewed', views.MostViewedNewsPostCategory.as_view(), name='most_viewed_news_category'),
    path('news/<str:news_cat_slug>/most_commented', views.MostCommentedNewsPostCategory.as_view(), name='most_commented_news_category'),
    
    # News Tag
    # News Tag List Details
    path('news/<str:slug>/tag', views.NewsTagList.as_view(), name='news_tag_list'),
    
    
    # All News Post List Filter
    path('latest/news', views.LastestNewsPostList.as_view(), name='latest_news'),
    path('most-read/news', views.MostReadNewsPostList.as_view(), name='most_read_news'),
    path('most-viewed/news', views.MostViewedNewsPostList.as_view(), name='most_viewed_news'),
    path('most-commented/news', views.MostCommentedNewsPostList.as_view(), name='most_commented_news'),
    
    
    
    # news_post_details 
     path('news/<str:news_post_slug>/post', views.NewsPostDetails.as_view(), name='news_post_details'), 
     
     # news comment post
    path('news/<int:pk>/news_comment', views.CreateNewsComment.as_view(), name='add_news_post_comment'),
    path('news/<int:pk>/update_comment', views.UpdateNewsComment.as_view(), name='update_news_post_comment'),
    
    #News Author
    path('news/<int:pk>/author', views.NewsAuthor.as_view(), name='news_author'),
    # All News Author Post List Filter
    path('latest/news/<int:pk>/post', views.LastestNewsAuthorPostList.as_view(), name='latest_news_author_post'),
    path('most-read/news/<int:pk>/post', views.MostReadNewsAuthorPostList.as_view(), name='most_read_news_author_post'),
    path('most-viewed/news/<int:pk>/post', views.MostViewedNewsAuthorPostList.as_view(), name='most_viewed_news_author_post'),
    path('most-commented/news/<int:pk>/post', views.MostCommentedNewsAuthorPostList.as_view(), name='most_commented_news_author_post'),
    
    
    
    
] 

