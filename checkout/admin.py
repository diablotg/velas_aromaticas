from django.contrib import admin
from .models import Address, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  #
    readonly_fields = ("product", "quantity", "get_total_price")

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "shipping_type", "total", "created_at")
    list_filter = ("status", "shipping_type", "created_at")
    search_fields = ("user__email", "id")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "last_name",
        "phone_number",
        "street_address",
        "city",
        "country",
        "is_default",
        "created_at",
    )
    list_filter = ("country", "is_default", "state")
    search_fields = (
        "user_email",
        "full_name",
        "last_name",
        "street_address",
        "city",
        "postal_code",
        "country",
    )
