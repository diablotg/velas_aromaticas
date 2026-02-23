import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from orders.models import Order
from .models import StripeEvent


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    # ---------------------------
    # 1️⃣ Verificar firma Stripe
    # ---------------------------
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    event_id = event.get("id")
    event_type = event.get("type")

    if not event_id or not event_type:
        return HttpResponse(status=400)

    # ---------------------------
    # 2️⃣ Idempotencia
    # ---------------------------
    if StripeEvent.objects.filter(stripe_event_id=event_id).exists():
        return HttpResponse(status=200)

    # ---------------------------
    # 3️⃣ Procesar evento
    # ---------------------------
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]

        metadata = session.get("metadata", {})
        order_id = metadata.get("order_id")

        if not order_id:
            return HttpResponse(status=400)

        with transaction.atomic():

            # Registrar evento primero (evita duplicados en concurrencia)
            StripeEvent.objects.create(stripe_event_id=event_id, event_type=event_type)

            order = Order.objects.select_for_update().filter(id=order_id).first()

            if not order:
                return HttpResponse(status=400)

            stripe_amount = session.get("amount_total")
            expected_amount = int(order.total * 100)

            if stripe_amount != expected_amount:
                return HttpResponse(status=400)

            # Solo marcar como pagada si no lo está
            if order.status != "PAID":
                order.status = "PAID"
                order.save(update_fields=["status"])

    else:
        # Registrar otros eventos sin procesarlos (opcional)
        StripeEvent.objects.create(stripe_event_id=event_id, event_type=event_type)

    return HttpResponse(status=200)
