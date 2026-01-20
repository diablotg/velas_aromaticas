from django.shortcuts import render
from products.models import Product
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET


def home(request):
    products = Product.objects.all()
    return render(request, "cart/catalog.html", {"products": products})


CART_SESSION_KEY = "cart"  # estructura: { "<product_id>": {"qty": int} }

# Para mostrar boton de carrito completo
show_cart_button = False
# ===============================


def _get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def _serialize_cart(cart):
    """
    Convierte la sesión (solo product_id + qty) a una lista con datos del producto
    para devolver al cliente.
    """
    items = []
    subtotal = Decimal("0.00")
    for pid, info in cart.items():
        try:
            product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            continue
        qty = int(info.get("qty", 0))
        line_total = product.price * qty
        subtotal += line_total
        items.append(
            {
                "id": product.id,
                "name": product.name,
                "price": str(
                    product.price
                ),  # str para evitar problemas de JSON con Decimal
                "price_display": f"{product.price:.2f}",
                "qty": qty,
                "line_total": str(line_total),
                "line_total_display": f"{line_total:.2f}",
                "image_url": (
                    product.image.url if getattr(product, "image", None) else None
                ),
            }
        )
    return {
        "items": items,
        "subtotal": str(subtotal),
        "subtotal_display": f"{subtotal:.2f}",
        "count": sum(i["qty"] for i in cart.values()),
    }


@require_GET
def cart_state(request):
    cart = _get_cart(request)
    data = _serialize_cart(cart)
    return JsonResponse({"success": True, "cart": data})


@require_POST
def cart_add(request):
    pid = request.POST.get("product_id")
    qty = int(request.POST.get("qty", 1))
    if not pid:
        return JsonResponse(
            {"success": False, "error": "product_id missing"}, status=400
        )
    # validaciones
    if qty < 1:
        return JsonResponse({"success": False, "error": "qty must be >= 1"}, status=400)
    # verificar producto existe
    product = get_object_or_404(Product, pk=pid)
    cart = _get_cart(request)
    entry = cart.get(str(product.id), {"qty": 0})
    entry["qty"] = entry.get("qty", 0) + qty
    cart[str(product.id)] = entry
    _save_cart(request, cart)
    return JsonResponse({"success": True, "cart": _serialize_cart(cart)})


@require_POST
def cart_remove(request):
    pid = request.POST.get("product_id")
    if not pid:
        return JsonResponse(
            {"success": False, "error": "product_id missing"}, status=400
        )
    cart = _get_cart(request)
    if str(pid) in cart:
        del cart[str(pid)]
        _save_cart(request, cart)
    return JsonResponse({"success": True, "cart": _serialize_cart(cart)})


@require_POST
def cart_update(request):
    pid = request.POST.get("product_id")
    qty = request.POST.get("qty")
    if not pid or qty is None:
        return JsonResponse({"success": False, "error": "params missing"}, status=400)
    try:
        qty = int(qty)
    except ValueError:
        return JsonResponse(
            {"success": False, "error": "qty must be integer"}, status=400
        )
    cart = _get_cart(request)
    if qty > 0:
        cart[str(pid)] = {"qty": qty}
    else:
        cart.pop(str(pid), None)
    _save_cart(request, cart)
    return JsonResponse({"success": True, "cart": _serialize_cart(cart)})
