from django.db import models
from django.conf import settings
from products.models import Product


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses"
    )
    full_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="México")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.street_address}, {self.city}, {self.country}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("creado", "Creado"),
        ("confirmado", "Confirmado"),
        ("enviado", "Enviado"),
        ("listo_recoleccion", "Listo para recolección"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    SHIPPING_CHOICES = [
        ("domicilio", "Domicilio"),
        ("tienda", "Entrega en tienda"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="creado")
    shipping_type = models.CharField(
        max_length=20, choices=SHIPPING_CHOICES, default="domicilio"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.email}"

    def calculate_total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        self.total = total
        self.save()
        return self.total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price
