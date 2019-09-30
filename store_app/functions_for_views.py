from .models import Cart


def get_or_create_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except (Cart.DoesNotExist, KeyError):
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        request.session['total'] = cart.items.count()
    return cart
