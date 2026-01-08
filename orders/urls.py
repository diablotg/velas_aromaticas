from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("success/<int:order_id>/", views.order_success, name="success"),
    path("status/<int:order_id>/", views.order_status, name="order_status"),
]
