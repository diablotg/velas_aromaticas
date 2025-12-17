from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout_view, name="checkout"),
    path("create-order/", views.create_order, name="create_order"),
]
