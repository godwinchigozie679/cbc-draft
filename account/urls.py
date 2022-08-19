from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from account.views import EditProfile, EditProfileAccount


   



urlpatterns = [ 
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"), 
    
    #   Activate
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name="activate"),
    
    # User_profile
    path('profile/<int:pk>/account', views.profile, name="profile"),
    # User Settings
     path('settings/<int:pk>/account', views.account_settings, name="account_settings"),
     
    # Change Password   
    path('password_change/', views.change_password, name='password_change'),
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    
    # edit Account and Profile
    path('account/<int:pk>/edit_account/', EditProfileAccount.as_view(), name='edit_account'),
    path('profile/<int:pk>/edit_profile/', EditProfile.as_view(), name='edit_profile'),
    
    # Delete Account 
    path('account/<int:pk>/delete/', views.DeleteAccount.as_view(), name='delete_account'),
    # Delete confirmation
    path('comfirm_delete/', views.confirm_delete, name='confirm_delete'),
 
] 


