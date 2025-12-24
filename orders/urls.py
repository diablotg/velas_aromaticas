from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("success/<int:order_id>/", views.order_success, name="success"),
]
