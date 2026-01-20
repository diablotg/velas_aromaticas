from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product_name",
        "price",
        "quantity",
        "line_total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "status",
        "total",
        "created_at",
    )

    inlines = [OrderItemInline]

    list_filter = ("status",)
    search_fields = ("id", "email")
    ordering = ("-created_at",)

    readonly_fields = (
        "subtotal",
        "shipping",
        "total",
        "created_at",
    )


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "delivery_type",
        "first_name",
        "last_name",
        "phone",
        "street",
        "interior",
        "neighborhood",
        "city",
        "state",
        "postal_code",
    )
