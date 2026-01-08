from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import render, redirect

from cart.views import _get_cart
from products.models import Product
from orders.models import Order, OrderItem, ShippingAddress

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout_view(request):
    cart = _get_cart(request)

    # =========================
    # Bloquear acceso sin carrito
    # =========================
    if not cart:
        return redirect("cart:home")

    # =========================
    # Preparar productos
    # =========================
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    order_items = []
    subtotal = Decimal("0.00")

    for product in products:
        quantity = int(cart[str(product.id)]["qty"])
        line_total = product.price * quantity
        subtotal += line_total

        order_items.append(
            {
                "product": product,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    shipping = Decimal("80.00")
    total = subtotal + shipping

    # =========================
    # POST → Crear orden + Stripe
    # =========================
    if request.method == "POST":
        email = request.POST.get("email")
        delivery_type = request.POST.get("delivery_type")

        if not email or not delivery_type:
            return render(
                request,
                "checkout/checkout.html",
                {
                    "order_items": order_items,
                    "subtotal": subtotal,
                    "shipping": shipping,
                    "total": total,
                    "error": "Información incompleta",
                },
            )

        # =========================
        # 1. Crear Order (UNPAID)
        # =========================
        order = Order.objects.create(
            email=email,
            subtotal=subtotal,
            shipping=shipping,
            total=total,
            delivery_type=delivery_type,
            status="UNPAID",
        )

        # =========================
        # 2. Crear OrderItems
        # =========================
        stripe_items = []

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product_id=item["product"].id,
                product_name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                line_total=item["line_total"],
            )

            stripe_items.append(
                {
                    "price_data": {
                        "currency": "mxn",
                        "product_data": {
                            "name": item["name"],
                        },
                        "unit_amount": int(item["price"] * 100),
                    },
                    "quantity": item["quantity"],
                }
            )

        # =========================
        # 3. ShippingAddress
        # =========================
        if delivery_type == "home":
            ShippingAddress.objects.create(
                order=order,
                delivery_type="home",
                first_name=request.POST.get("first_name", ""),
                last_name=request.POST.get("last_name", ""),
                phone=request.POST.get("phone", ""),
                street=request.POST.get("street", ""),
                interior=request.POST.get("interior", ""),
                neighborhood=request.POST.get("neighborhood", ""),
                city=request.POST.get("city", ""),
                state=request.POST.get("state", ""),
                postal_code=request.POST.get("postal_code", ""),
            )
        else:
            ShippingAddress.objects.create(
                order=order,
                delivery_type="pickup",
                pickup_location="Av. Central #250, Querétaro, Qro.",
            )

        # =========================
        # 4. Stripe Checkout Session
        # =========================
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=stripe_items,
            success_url=f"http://127.0.0.1:8000/orders/success/{order.id}/",
            cancel_url="http://127.0.0.1:8000/checkout/",
            metadata={
                "order_id": str(order.id),
            },
        )

        return redirect(session.url, code=303)

    # =========================
    # GET → Render checkout
    # =========================
    return render(
        request,
        "checkout/checkout.html",
        {
            "order_items": order_items,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total,
        },
    )
