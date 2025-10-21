import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from checkout.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Pedido #" + str(order.id)},
                    "unit_amount": int(order.total * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/success/",
        cancel_url="http://localhost:8000/cancel/",
        metadata={"order_id": str(order.id)},
    )

    return JsonResponse({"id": session.id})
