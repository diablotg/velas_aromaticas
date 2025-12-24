import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(order, request):
    """
    Crea una sesión de Stripe Checkout a partir de una Order
    """

    line_items = []

    for item in order.items.all():
        line_items.append(
            {
                "price_data": {
                    "currency": "mxn",
                    "product_data": {
                        "name": item.product.name,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            }
        )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        customer_email=order.email,
        success_url=request.build_absolute_uri(
            f"/payments/success/?order_id={order.id}"
        ),
        cancel_url=request.build_absolute_uri("/checkout/"),
        metadata={
            "order_id": order.id,
        },
    )

    return session
