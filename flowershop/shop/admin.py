from django.contrib import admin

# Register your models here.
from .models import Customer, Bouquet, Order, Courier, Florist, Payment

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")
    search_fields = ("name", "phone")

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "occasion")
    search_fields = ("name", "description")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "bouquet", "status", "delivery_time")
    list_filter = ("status",)
    search_fields = ("customer__name", "address")

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")

@admin.register(Florist)
class FloristAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "payment_id", "status")