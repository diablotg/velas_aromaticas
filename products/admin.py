from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "image_tag")
    search_fields = ("name",)
    list_filter = ("price",)
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="90" height="90" />')
        return "Sin imagen"

    image_tag.short_description = "Vista previa"

    image_tag.allow_tags = True
