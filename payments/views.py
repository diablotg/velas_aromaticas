import stripe
import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Evento más importante
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        order_id = session["metadata"].get("order_id")

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = "PAID"
                order.save()
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)
