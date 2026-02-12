from django.shortcuts import get_object_or_404, render
from cart.views import _save_cart
from .models import Order
from django.http import JsonResponse


def order_success(request, public_id):
    order = get_object_or_404(Order, public_id=public_id)

    session_public_id = request.session.get("last_order_public_id")

    if not session_public_id or str(order.public_id) != session_public_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

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


def order_status(request, public_id):
    order = get_object_or_404(Order, public_id=public_id)

    session_public_id = request.session.get("last_order_public_id")

    if session_public_id != str(order.public_id):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    return JsonResponse({"status": order.status})
