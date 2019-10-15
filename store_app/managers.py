from django.db import models


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
