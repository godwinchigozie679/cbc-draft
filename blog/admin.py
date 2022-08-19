from django.contrib import admin
from blog.models import Category, SubCategory, Post, NewsPost, NewsCategory, NewsSubCategory, NewsComment, BlogComment, Advert
from mptt.admin import MPTTModelAdmin
# Register your models here.





# Blog Category Admin
class SubCategoryAdmin(admin.TabularInline):
    model = SubCategory

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryAdmin,
    ]


admin.site.register(Category, CategoryAdmin)

# Advert
admin.site.register(Advert)

#Blog
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'sub_category', 'author', 'status', 'publish', 'views',)
    list_filter = ('status', 'created_on', 'publish', 'author', 'views', 'category',)
    search_fields = ('title', 'content')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

# News
@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'sub_category', 'author', 'status', 'publish','views',)
    list_filter = ('status', 'category', 'created_on', 'publish', 'author', 'views',)
    search_fields = ('title', 'content')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    
# Blog Comment
# @admin.register(BlogComment)
# class BlogCommentAdmin(admin.ModelAdmin):
#     list_display = ('blog_post', 'author', 'publish', 'status',)
#     list_filter = ('blog_post', 'author', 'publish', 'status',)
#     search_fields = ('news_post', 'author', 'publish',)    
#     date_hierarchy = 'publish'
#     ordering = ('status', 'publish')
admin.site.register(BlogComment, MPTTModelAdmin)  
admin.site.register(NewsComment, MPTTModelAdmin)    
  


# News Comment
# @admin.register(NewsComment)
# class NewsCommentAdmin(admin.ModelAdmin):
#     list_display = ('news_post', 'author', 'publish', 'status',)
#     list_filter = ('news_post', 'author', 'publish', 'status',)
#     search_fields = ('news_post', 'author', 'publish',)    
#     date_hierarchy = 'publish'
#     ordering = ('status', 'publish')

class NewsSubCategoryAdmin(admin.TabularInline):
    model = NewsSubCategory

class NewsCategoryAdmin(admin.ModelAdmin):
    inlines = [
        NewsSubCategoryAdmin,
    ]


admin.site.register(NewsCategory, NewsCategoryAdmin)
  