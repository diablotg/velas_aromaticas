from django.contrib import admin
from .models import Address


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
