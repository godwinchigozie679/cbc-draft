from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from account.models import Profile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Password Change
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
# Password Reset



#
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse_lazy

from django.core.mail import send_mail

from account.models import Account

from account.forms import RegistrationForm, AccountAuthenticationForm, EditProfileAccountForm, EditProfileForm

from src import settings

# import course
from e_learning.models.course import Course

# Import current Site
from django.contrib.sites.shortcuts import get_current_site

# loader
from django.template.loader import render_to_string
# uid
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# focer_bytes and forced text
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth.tokens import default_token_generator
# Import generate Token
from account.gft.token import generate_token
# import mail
from django.core.mail import EmailMessage, send_mail,  BadHeaderError

# Threading
import threading

# force login
from django.contrib.auth.decorators import login_required


# GENERICS FOR Account Delete
from django.views import generic
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm




# Threading for sending email and performing asynchronous task

class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()



# Confirmation/activation email
def send_activation_email(request, user):
    
    current_site = get_current_site(request)
    email_subject = 'Confirm your email @ CBC - Community!!'
    message2 = render_to_string('confirmation/account_email_confirm.html', {
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            
    email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            
    email.fail_silently = True
    
    EmailThread(email).start() # This is from the threading constructed above
    
    return send_activation_email
    
    
# Registration view
def register_view(request):
     
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            user.save()
            
            profile = Profile()
            profile.user = user
            profile.save()
            
            success_message = 'Your account is successfully created.'             
            success_message += ' Please check your email inbox or spam to activate your account.'
            messages.success(request, success_message)
               
            # Welcome Message
            subject = 'Welcome to CBC community'
            message = 'hello '
            message += user.first_name + ' ' + user.last_name + '!! \n'
            message += ' Welcome to CBC. Thank you for visiting our website.'
            message += ' \n We have sent you a confirmation email, please confirm your email address in order to activate your account.'
            message += ' \n\n Thanking you \n\n CBC Team'
            
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently = True)
            
            send_activation_email(request, user)
        
            return redirect(reverse('login'))     
        else: 
            messages.warning(request, 'Invalid Registration Details')
            # messages.warning(request, form.errors)
    
    else:        
        form = RegistrationForm()    
        
    
    context = {
            'form': form,
        }
        
    return render(request, template_name='registration/register.html', context=context )

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# Activate
def activate(request, uidb64, token):
    try:
       uid = force_str(urlsafe_base64_decode(uidb64)) 
       user = Account.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email verified you can now login')
        
        return redirect(reverse('login'))
       
    else:
        return render(request, template_name='confirmation/account_activation_failed.html')

    context = {'uidb64':uidb64, 'token':token}
    
    return render(request, template_name='confirmation/account_email_confirm.html', context=context)


# Logout
def logout_view(request):
    
    logout(request)
            
    return render(request, template_name='registration/loggedout.html')

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# Login
def login_view(request):
    
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}. Go to <a href='/'>home</a>")
     
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
              
        if form.is_valid():
            email = form.cleaned_data.get("email")
            
            password = form.cleaned_data.get("password")
            
            user = authenticate(request, email=email, password=password)
            
            try:
                if not user.is_email_verified:
                    messages.warning(request, 'Your email is not verified. Please, check your email inbox or spam.')
                    send_activation_email(request, user)
                    return redirect(reverse('login')) 
                else:    
                    if user is not None:
                        login(request, user)
                        # if user.is_author:
                        #     return HttpResponse('..Author')
                        # elif user.is_admin:
                        #     return HttpResponse('..admin')
                        # else:
                        return redirect(reverse('user_course'))
                    
                    else:
                        messages.warning(request, 'Email OR Password is incorrect')
                
            except:
                messages.warning(request, 'Email OR Password is incorrect')      
                return redirect(reverse('login'))
    else:         
        form = AccountAuthenticationForm()
        
    
    context = {
        'form':form,
        
    }
    
    return render(request, template_name='registration/login.html', context=context)


# User Profile
# @login_required(login_url='login')
def profile(request, pk):
    user = request.user    
    profile = Profile.objects.get(user__id=user.id)
        
    context = {        
        'profile': profile,
        
    }
    
    return render(request, template_name='account_crud/user_profile.html', context=context)


# Change Password
@login_required
def change_password(request):
    if request.method == 'POST':        
        form = PasswordChangeForm(request.user, request.POST)        
        if request.POST['old_password'] == '' and request.POST['new_password2'] == '' and request.POST['new_password1'] == '':
            messages.warning(request, 'Fields must not be empty!')
            return redirect('password_change')
        
        
        if request.POST['old_password'] == request.POST['new_password1']:
            messages.warning(request, 'Your old and new password must not be the same!')
            return redirect('password_change')
        
        
            
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse_lazy('password_change_success'))
        else:
            messages.warning(request, ('Invalid details provided. Please try changing your password again.'))
    
    
    else:
        form = PasswordChangeForm(request.user)
    return render(request, template_name='account_crud/password_change_form.html')

# password_change_success
def password_change_success(request):
    return render(request, template_name='account_crud/password_change_success.html')
 
 
# Edit Account/Settings
class EditProfileAccount(generic.UpdateView):
    form_class = EditProfileAccountForm
    model = Account       
    template_name = 'account_crud/edit_account_settings.html'  
      
        
    # Post the data into the DB
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        account = get_object_or_404(Account, pk=pk)
        form = EditProfileAccountForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            edit_account = form.save(commit=False)
            form.instance = self.request.user
            print(edit_account)  # Print so I can see in cmd prompt that something posts as it should
            edit_account.save()
            return redirect('account_settings', user.id)
        
        try:
            return render(request, {'form': 'form'})
        except:
            
            messages.warning(request, 'The username provided is in use already. Please try another username.')
            return redirect('edit_account', user.id)
        
        




# Edit Profile
class EditProfile(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login'
    redirect_field_name = 'next'
    
    model = Profile
    form_class = EditProfileForm    
    template_name = 'account_crud/edit_profile.html'    
        
    # Post the data into the DB
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, pk=pk)
        form = EditProfileForm(request.POST, instance=profile)        
        if form.is_valid():
            edit_profile = form.save(commit=False)
            form.instance = self.request.user
            print(edit_profile)  # Print so I can see in cmd prompt that something posts as it should
            edit_profile.save()
            return redirect('profile', user.id)
        return render(request,  {'form': form})


# Seetings
def account_settings(request, pk):
    user = request.user    
    user_account = Account.objects.get(pk=user.id)
    
    context = {        
        'user_account': user_account,        
    }
    
    return render(request, template_name='account_crud/setting_profile.html', context=context)
#  DELETE ACCOUNT

class DeleteAccount(generic.DeleteView):
    # specify the model you want to use
    model = Account
    template_name = 'account_crud/confirm_delete_account.html'
    success_url = reverse_lazy('confirm_delete')
    
       
# confirm_delete
def confirm_delete(request):
    return redirect(reverse('home'))




          