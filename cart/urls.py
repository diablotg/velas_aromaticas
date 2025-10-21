from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("api/cart/", views.cart_state, name="cart_state"),  # GET
    path("api/cart/add/", views.cart_add, name="cart_add"),  # POST
    path("api/cart/remove/", views.cart_remove, name="cart_remove"),  # POST
    path("api/cart/update/", views.cart_update, name="cart_update"),  # POST
]
