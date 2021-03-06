from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from .managers import CustomProductManager, CartManager
from decimal import Decimal
from django.conf import settings
from users.models import User


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
    users = models.ManyToManyField(User, blank=True, related_name='products')
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

    class Meta:
        ordering = ['id']


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        product = Product.objects.get(slug=product_slug)
        for item in self.items.all():
            if item.product.name == product.name:
                return
        new_item = CartItem(product=product, item_total=product.price)
        new_item.save()
        self.items.add(new_item)
        self.save()

    def remove_from_cart(self, product_slug):
        product = Product.objects.get(slug=product_slug)
        for cart_item in self.items.all():
            if cart_item.product.name == product.name:
                self.items.remove(cart_item)
                self.save()
                cart_item.delete()
                return

    @staticmethod
    def get_category(product_slug):
        product = Product.objects.get(slug=product_slug)
        return product.category.slug

    def update_total_price(self):
        self.cart_total = Decimal(0)
        for item in self.items.all():
            self.cart_total += item.item_total
        self.save()
        return self.cart_total

    def get_product_items(self):
        ls = [item.product.name for item in self.items.all()]
        return ls

    def get_products_quantity(self):
        quantity_of_products = 0
        for item in self.items.all():
            quantity_of_products += item.quantity
        return quantity_of_products


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    buying_type = models.CharField(max_length=40,
                                   choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')),
                                   default='Самовывоз')
    address = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES)


def pre_save_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(translit(instance.name, reversed=True))


pre_save.connect(pre_save_slug_field, sender=Category)
pre_save.connect(pre_save_slug_field, sender=Product)
