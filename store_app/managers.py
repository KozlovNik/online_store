from django.db import models


class CustomProductManager(models.Manager):
    # Выводятся все доступные товары
    def all(self, *args, **kwargs):
        return super().get_queryset().filter(available=True)

