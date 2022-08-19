from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from e_learning.models.user_course import UserCourse, AuthorCourse
from django.contrib import messages
from e_learning.models.course import Course
from account.models import Account
from e_learning.models.video import Video
from e_learning.templatetags import course_custom_tags
from .models import Payment, PaymentExchangeRate
from time import time
from pypaystack import Transaction, Customer, Plan
import json
from django.http import JsonResponse
import math
# import secrets

from src.settings import *



########################################################################################
# Checktout
def checkout(request, slug):    
    course = Course.objects.get(slug=slug)
    
    if not request.user.is_authenticated:
        return redirect('login')  
        return redirect('initiate_payment')
    
    context = {'course': course,}
        
    return render(request, template_name='check_out.html', context=context)

########################################################################################

# Payment option
def initiate_payment(request, slug):    
    course = Course.objects.get(slug=slug)   
    order = None
    user = request.user
    error = None     
     
    paymentMethod = request.GET.get('paymentMethod')
    #Paystack Gateway
    if paymentMethod == 'paystack':
                
        try:            
            user_course = UserCourse.objects.get(course=course, user=user)
            
            error = 'You Are Already Enrolled in this Course'
        except:
            pass      
        
            return redirect('initiate_paystack', slug=slug)            
        
    # Paypal Gateway
    
    context = {'course': course,
               'order': order,
                'error': error,
                                
               }  
      
    return render(request, template_name='initiate_payment.html',context=context)

########################################################################################



# Initiate Paystack
def initiate_paystack(request, slug):
    course = Course.objects.get(slug=slug)
    order = None    
    user = request.user
    error = None   
    
    # Exchange
    exchange_rate = str(PaymentExchangeRate.objects.all()[0])     
        
         
    amount = int(course.price - (course.price * course.percentage_discount * 0.01)) *100 * int(exchange_rate)  
    
      
            
    payment = Payment()
    
    payment.course = course
    payment.user = user 
    payment.author_course = course.author
    payment.amount = amount 
    payment.order_id
    payment.save()    
            
    order_id = payment.order_id
    amount = payment.amount
    slug = course.slug
            
            
            
    paystack_secret_key = 'sk_test_91ea127069a2e935c5dd98f51de416fa8a0a80ab'
    paystack_public_key = 'pk_test_52299579c0d5504d20141c1092f8b3022f085e7c'
                
            
    context = {
                'course': course,
                'user': user,
                'amount': amount,
                'order_id': order_id,
                'slug':slug,
                'paystack_secret_key': paystack_secret_key,
                'paystack_public_key': paystack_public_key,
                
                
            }
            
    return render(request, template_name='paystack.html', context=context)




# VERIFY PAYSTACK PAYMENT      
      
def verify_paystack_payment(request, order_id, slug): 
    payment = get_object_or_404(Payment,order_id=order_id, course__slug=slug)   
    
    
    # Exchange
    exchange_rate = str(PaymentExchangeRate.objects.all()[0]) 
    
    try:
        paystack_secret_key = 'sk_test_91ea127069a2e935c5dd98f51de416fa8a0a80ab'
        transaction = Transaction(authorization_key=paystack_secret_key, )
        response = transaction.verify(order_id) 
        
        
        
        paystack_payment_id = response[3]['customer']['customer_code']
        paystack_payment_order_id = response[3]['reference']
        amount = response[3]['amount']
        
        payment.payment_id = paystack_payment_id
        payment.order_id = paystack_payment_order_id
        payment.verified = True  
        payment.amount = amount/(100 * int(exchange_rate))
        
       
          
        # Update Author Ordered Course 
        # authorCourse = AuthorCourse(user= payment.author_course, course=payment.course)         
        # authorCourse.save() 
        
        
        # Update User Course Paid Course
        userCourse = UserCourse(user= payment.user, course=payment.course)                         
        userCourse.save()  
        
        payment.user_course = userCourse        
        payment.save()         
        
        
        # user_course_module = UserModule.objects.create(user_course=userCourse, user_course_module=)
        
        return redirect('course_success_payment', slug)
    except:
        return HttpResponse('Invalid Payment Details.')
    
    
#########################################################################################