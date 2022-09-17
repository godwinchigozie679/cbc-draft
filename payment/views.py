from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from e_learning.models.user_course import UserCourse
from django.contrib import messages
from e_learning.models.course import Course
from account.models import Account
from e_learning.models.video import Video
from e_learning.templatetags import course_custom_tags
from .models import Payment, PaymentExchangeRate
from payment.author_commission_models import AuthorCommision
from time import time
# from pypaystack import Transaction, Customer, Plan
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction #delete if it doesn't work

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
            
    reference = payment.order_id
    amount = payment.amount
    slug = course.slug
    
         
            
            
    paystack_secret_key = 'sk_test_ddd359b5ad1643d940d6c2fc8d0dec2ccca74f07'
    paystack_public_key = 'pk_test_52299579c0d5504d20141c1092f8b3022f085e7c'
                
            
    context = {
                'course': course,
                'user': user,
                'amount': amount,
                'reference': reference,
                'slug':slug,
                'paystack_secret_key': paystack_secret_key,
                'paystack_public_key': paystack_public_key,
                
                
            }
            
    return render(request, template_name='paystack.html', context=context)




# VERIFY PAYSTACK PAYMENT      
      
def verify_paystack_payment(request, reference, slug): 
    payment = get_object_or_404(Payment, order_id=reference, course__slug=slug)   
    
    print('verify payment console...')
    # Exchange
    exchange_rate = str(PaymentExchangeRate.objects.all()[0]) 
    
    try:
        paystack_secret_key = 'sk_test_ddd359b5ad1643d940d6c2fc8d0dec2ccca74f07'
        paystack = Paystack(secret_key=paystack_secret_key)       
        response = paystack.transaction.verify(reference)
        
        paystack_payment_id = response['data']['id']
        paystack_payment_order_id = response['data']['reference']
        amount = response['data']['amount']
        
        payment.payment_id = paystack_payment_id
        payment.order_id = paystack_payment_order_id
        payment.verified = True  
        payment.amount = amount/(100 * int(exchange_rate))
        
       
          
        
        
        
        # Update User Course Paid Course
        per_comm = AuthorCommision.objects.all()[0]
        
        amount = payment.amount
        author_comm = (amount * float(str(per_comm)))/100 
        
        userCourse = UserCourse(user= payment.user, 
                                course=payment.course, 
                                percentage_commision=per_comm, 
                                commission=author_comm)                         
        
        userCourse.save()  
        
        payment.user_course = userCourse        
        payment.save()   
        
        return redirect('course_success_payment', slug)
    except:
        return HttpResponse('Invalid Payment Details.')
    
    
#########################################################################################