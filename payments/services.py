from orders.models import Order


def mark_order_as_paid(order_id: int):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return False

    if order.status == "PAID":
        return True  # idempotente

    order.status = "PAID"
    order.save(update_fields=["status"])
    return True
