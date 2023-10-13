from django.contrib import admin


from .models import Order, Contact, Bid
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_shipper")

admin.site.register(Contact, CustomerAdmin)

admin.site.register(Order)
admin.site.register(Bid)