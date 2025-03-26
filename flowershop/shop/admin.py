from django.contrib import admin
from .models import (
    Customer,
    Bouquet,
    Order,
    Courier,
    Florist,
    Payment,
    Statistics,
    Consultation,
)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "phone", "created_at")
    list_filter = ("created_at",)


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ("get_customer_name", "get_bouquet_name", "quantity", "order_date")

    def get_customer_name(self, obj):
        return obj.customer_name.name

    get_customer_name.short_description = "Заказчик"

    def get_bouquet_name(self, obj):
        return obj.bouquet_name.name

    get_bouquet_name.short_description = "Букет"


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
