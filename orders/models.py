from django.db import models
import uuid


class Order(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True
    )

    STATUS_CHOICES = (
        ("UNPAID", "No pagado"),
        ("PAID", "Pagado"),
        ("CANCELLED", "Cancelado"),
    )

    email = models.EmailField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    delivery_type = models.CharField(
        max_length=10,
        choices=(("home", "Domicilio"), ("pickup", "Recolección")),
        default="pickup",
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="UNPAID")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, related_name="shipping_address", on_delete=models.CASCADE
    )

    delivery_type = models.CharField(
        max_length=10,
        choices=(("home", "Domicilio"), ("pickup", "Recolección")),
        default="pickup",
    )

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    street = models.CharField(max_length=255, blank=True)
    interior = models.CharField(max_length=50, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
