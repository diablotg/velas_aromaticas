from django.db import models


class StripeEvent(models.Model):
    stripe_event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stripe_event_id} - {self.event_type}"
