from django.contrib import admin
from payment.models import Payment, PaymentExchangeRate

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ["payment_id","order_id","user", "author_course","course", "verified","amount"]
    list_filter = ['course', 'verified',]

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentExchangeRate)