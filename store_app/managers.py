from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class CustomProductManager(models.Manager):
    # Выводятся все доступные товары
    def all(self, *args, **kwargs):
        return super().get_queryset().filter(available=True)

    def user_favorites_quantity(self, request):
        try:
            quantity = len(self.get_queryset().filter(users=request.user).all())
        except TypeError:
            quantity = 0
        return quantity

    def get_favorites_or_none(self, user):
        try:
            user_favorites_products = self.filter(users=user).all()
        except TypeError:
            user_favorites_products = None
        return user_favorites_products


class CartManager(models.Manager):
    def get_or_create_cart(self, request):
        try:
            cart = self.get(id=request.session['cart_id'])
        except (ObjectDoesNotExist, KeyError):
            cart = self.create()
            request.session['cart_id'] = cart.id
        return cart
