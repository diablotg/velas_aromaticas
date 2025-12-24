def get_server_cart(request):
    """
    Devuelve el carrito almacenado en la sesión.
    Si no existe, regresa un dict vacío.
    """

    cart = request.session.get("cart")

    if cart is None:
        cart = {}
        request.session["cart"] = cart

    return cart
