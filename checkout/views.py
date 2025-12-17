# checkout/views.py
from django.shortcuts import render
from products.models import Product
from decimal import Decimal
from cart.views import _get_cart  # o usar tu propia util en cart/utils

# si prefieres no importar _get_cart de views, mueve la lógica a utils y úsala desde ambos lados


def checkout_view(request):
    cart = _get_cart(request)  # carrito en sesión: {product_id: {"qty": X}, ...}
    items = []
    total = Decimal("0.00")

    for pid, info in cart.items():
        try:
            product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            continue
        qty = info.get("qty", 0)
        line_total = product.price * qty
        total += line_total
        items.append(
            {
                "product": product,
                "qty": qty,
                "line_total": line_total,
            }
        )

    return render(
        request,
        "checkout/checkout.html",
        {
            "items": items,
            "total": total,
        },
    )
