from django.contrib import admin
from django.urls import path
from payment.views import checkout
from payment import views
# from e_learning.models.course import Course


# from account.views import  




urlpatterns = [         
    path('check-out/<str:slug>', views.checkout, name='checkout'),
    path('initiate_payment/<str:slug>', views.initiate_payment, name='initiate_payment'),
    path('<str:slug>/paystack', views.initiate_paystack, name='initiate_paystack'),
    path('paystack/<str:order_id>/<slug:slug>', views.verify_paystack_payment, name='verify_paystack_payment'),
    
] 