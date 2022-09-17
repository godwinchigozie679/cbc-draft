from e_learning.models.course_review import Review
from django import forms
from account.models import AuthorBankAccount


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment',]

"""Blog Creation Form"""
class BankAccountCreationForm(forms.ModelForm):    
    bank_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-content-input my-3','placeholder': 'Add Bank Name'})) 
    account_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-content-input my-3','placeholder': 'Add Account Name'}))
    account_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-content-input my-3','placeholder': 'Add Account Number'}))       
    

    class Meta:
        model = AuthorBankAccount
        fields = ['bank_name', 'account_name', 'account_number',]
        
        
