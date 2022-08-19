from django.contrib import admin

# Register your models here.
from social_handle.models import SocialHandle, Social, PhoneNumber, Email, OfficeAdress



class SocialAdmin(admin.TabularInline):
    model = SocialHandle

class SocialHandleAdmin(admin.ModelAdmin):
    inlines = [
        SocialAdmin,
    ]


admin.site.register(SocialHandle)
admin.site.register(Social, SocialHandleAdmin)
admin.site.register(PhoneNumber)
admin.site.register(Email)
admin.site.register(OfficeAdress)