from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("success/<uuid:public_id>/", views.order_success, name="success"),
    path("status/<uuid:public_id>/", views.order_status, name="order_status"),
]
