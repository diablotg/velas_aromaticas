import json
from django.http import JsonResponse
from products.models import Product
from .models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        cart_data = request.COOKIES.get("cart")
        cart = json.loads(cart_data) if cart_data else {}
    except:
        return JsonResponse({"error": "Carrito inválido"}, status=400)

    if not cart:
        return JsonResponse({"error": "El carrito está vacío"}, status=400)

    order = Order.objects.create(total=0)

    cart_total = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue  # ignorar productos inválidos

        quantity = item.get("quantity", 0)

        # Validar cantidades
        if quantity < 1 or quantity > 20:
            continue

        # Nunca usamos el precio que viene del cliente
        price = product.price

        line_total = price * quantity
        cart_total += line_total

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price,
            subtotal=line_total,
        )

    order.total = cart_total
    order.save()

    return JsonResponse({"order_id": order.id})
