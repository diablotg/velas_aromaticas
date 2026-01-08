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
