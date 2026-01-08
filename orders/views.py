from django.shortcuts import get_object_or_404, render
from cart.views import _save_cart
from .models import Order
from django.http import JsonResponse


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # 🔥 Vaciar carrito cuando el usuario regresa de Stripe
    _save_cart(request, {})

    return render(
        request,
        "orders/success.html",
        {
            "order": order,
            "items": order.items.all(),
        },
    )


def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({"status": order.status})
