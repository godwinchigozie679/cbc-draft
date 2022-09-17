from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, FormView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from e_learning.models.course import Course
from e_learning.models.course_modules import Modulee
from e_learning.models.video import Video
from e_learning.models.user_course import UserCourse
from e_learning.models.quiz import Result
from account.models import AuthorBankAccount
from e_learning.views import  homepage, course_video, user_course, course_page
from datetime import date, datetime
from django.db.models import Q
import datetime as dt
from payment.models import Payment
from django.db.models import Sum
from e_learning.models.course_forms import BankAccountCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone



# Paginator
from django.core.paginator import Paginator

#Login Decorator
from django.contrib.auth.decorators import login_required

#######################################################################################
@login_required(login_url='login')
def author_dashboard(request):
    
    today = date.today()
    
    user = request.user  
    
    # Today Sales Unit
    today_order = UserCourse.objects.filter(course__author=user, date__date=today).count()
    
    
    # Today Commission
    today_earnings = UserCourse.objects.filter(course__author=user, 
            date__date=today).aggregate(Sum('commission'))['commission__sum']
    
    
    # Total Sales Unit
    all_time_order = UserCourse.objects.filter(course__author=user).count()
    
    
    # Total Course Commission
    total_earnings = UserCourse.objects.filter(course__author=user
                                ).aggregate(Sum('commission'))['commission__sum']
    
    
    
    # total course
    total_courses = Course.objects.filter(author=user).count()
    
    # Month Earning
    current_month = datetime.now().month    
    
    month_earnings = UserCourse.objects.filter(course__author=user, date__month=current_month
                                ).aggregate(Sum('commission'))['commission__sum']
    
    context = {
        'today_order':today_order,
        'today_earnings': today_earnings,
        'all_time_order': all_time_order,
        'total_earnings': total_earnings,
        'month_earnings': month_earnings,
        'total_courses': total_courses,
        
       
    }
    
    return render(request, template_name='courses/dashboard/author-dashboard/author.html', context=context) 
  

class AuthorCourse(LoginRequiredMixin, ListView):
    
    def get_queryset(self):        
        return Course.objects.filter(author=self.request.user)  
    
    context_object_name = 'courses'
    
    paginate_by = 3   
    
    template_name='courses/dashboard/author-dashboard/author_courses.html' 
        
    
@login_required(login_url='login')     
def bank_account_details(request):
        
    bank_acount_detail = None
    
    try:    
        bank_acount_detail = AuthorBankAccount.objects.get(user=request.user)
       
    except Exception:
        pass
        
    
    context = {'bank_acount_detail': bank_acount_detail} 
    
    template_name='courses/dashboard/author-dashboard/account_detail.html'   
       
    return render(request, template_name=template_name, context=context)


class AddBankAccountDetails(LoginRequiredMixin, CreateView):
    
    login_url = '/login'
    
    redirect_field_name = 'next'
            
    template_name = 'courses/dashboard/author-dashboard/author_bank_account_creation_form.html'
        
    model = AuthorBankAccount
        
    form_class = BankAccountCreationForm
        
    def form_valid(self, form):                    
        form.instance.user = self.request.user 
        
        if not form.instance.bank_name:
            return redirect('add_bank_details')#I will come back
            
        return super().form_valid(form)
    
        if not form.instance.account_name:
            return redirect('add_bank_details')#I will come back
        
        if not form.instance.account_number:
            return redirect('add_bank_details')#I will come back
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        
        messages.success(
            self.request, 'Your Account Details is Added successfully.')
        
        return reverse('bank_details') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_detail"] = None
        try:
            context["bank_detail"] = AuthorBankAccount.objects.get(user=self.request.user)
        except:
            pass
        return context   
    




    #Uodate View
class EditBankAccountDetails(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'next'
    
    model = AuthorBankAccount            
    
    form_class = BankAccountCreationForm
       
    template_name = 'courses/dashboard/author-dashboard/author_bank_account_creation_form.html'    
        
    # Post the data into the DB
    def post(self, request, pk, *args, **kwargs):
        user = self.request.user        
        user_bank_detail = AuthorBankAccount.objects.get(pk=self.kwargs['pk'])        
        form = BankAccountCreationForm(request.POST, instance=user_bank_detail) 
              
        if form.is_valid():
            edit_user_bank_detail = form.save(commit=False)
            form.instance = self.request.user                       
            edit_user_bank_detail.save()
            return redirect('bank_details')
        return render(request,  {'form': form})

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["bank_detail"] = None
            try:
                context["bank_detail"] = AuthorBankAccount.objects.get(user=self.request.user)
            except:
                pass
            return context
        
        
# Earnings
def earnings(request):
    
    user = request.user
    
    
    
    #Current Data    
    currentDate = timezone.now() 
    
    print(currentDate, 'current date -----')
    #First Day Date in a month
    firstDayOfMonth = dt.date(currentDate.year, currentDate.month, 1)
    
    # firstDayOfMonth = timezone(currentDate.year, currentDate.month, 1)
    print(firstDayOfMonth, 'first day -----')
    
    todays_earnings = UserCourse.objects.filter(course__author=user,date__gte=firstDayOfMonth, date__lte=currentDate)
    y_axis = [p.commission for p in todays_earnings]       
    print(y_axis, 'commision ')
    
    today = [day for day in range(date.today().day+1)]    
    today.pop(0)
    print(today, 'date')
    
    
    
    
    
    template_name = 'courses/dashboard/author-dashboard/earnings.html'
    context = {}
    
    return render(request, template_name=template_name, context=context)