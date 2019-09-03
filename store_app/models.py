from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from .managers import CustomProductManager


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория', unique=True)
    slug = models.SlugField(verbose_name='Поле слага', unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cat', kwargs={'category_slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Бренд', null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return '{0}/{1}'.format(instance.slug, filename)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название товара')
    slug = models.SlugField(null=True, blank=True, verbose_name='Поле слага')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(verbose_name='Изображение', upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name='Наличие товара')
    custom_objects = CustomProductManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={'product_slug': self.slug, 'category_slug': self.category.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return 'Карточка для продукта {0}'.format(self.product.name)


class Cart(models.Model):
    item = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)


def pre_save_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(translit(instance.name, reversed=True))


pre_save.connect(pre_save_slug_field, sender=Category)
pre_save.connect(pre_save_slug_field, sender=Product)
