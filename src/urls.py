
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
# for static file

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('e_learning.urls')),     
    path('', include('account.urls')),
    path('', include('payment.urls')),
    path('', include('blog.urls')),  
    path('ckeditor', include('ckeditor_uploader.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)