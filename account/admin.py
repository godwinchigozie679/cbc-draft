from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Profile

from .models import Account
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name','email', 'date_joined', 'last_login','is_author', 'is_admin', 'is_staff',)
    search_fields = ('email',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    ordering = ('email',)
    

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)