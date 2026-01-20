import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(order):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "mxn",
                    "product_data": {
                        "name": f"Pedido #{order.id}",
                    },
                    "unit_amount": int(order.total * 100),
                },
                "quantity": 1,
            }
        ],
        metadata={
            "order_id": str(order.id),
        },
        success_url=f"http://127.0.0.1:8000/orders/success/{order.id}/",
        cancel_url="http://127.0.0.1:8000/cart/",
    )

    return session


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
