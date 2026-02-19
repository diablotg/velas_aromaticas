from django.db import models


class StripeEvent(models.Model):
    stripe_event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stripe_event_id
