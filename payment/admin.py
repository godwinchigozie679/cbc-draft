from django.contrib import admin
from payment.models import Payment, PaymentExchangeRate
from payment.author_commission_models import AuthorCommision

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ["payment_id","order_id","user", "author_course","course", "verified","amount"]
    list_filter = ['course', 'verified',]

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentExchangeRate)
admin.site.register(AuthorCommision)