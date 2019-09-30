from django.shortcuts import render
from store_app.models import Product, Category, Brand, Cart, CartItem
from django.http import HttpResponseRedirect, Http404, JsonResponse
from .functions_for_views import get_or_create_cart
from django.urls import reverse
from decimal import Decimal


def index(request):

    products = Product.objects.all()
    cart = get_or_create_cart(request)
    products_list = cart.get_product_items()
    context = {
        'products': products,
        'cart': cart,
        'products_list': products_list,
    }
    return render(request, 'store_app/index.html', context)


def show_category(request, **kwargs):
    cart = get_or_create_cart(request)
    products_list = cart.get_product_items()
    try:
        category = Category.objects.get(slug=kwargs['category_slug'])
    except Category.DoesNotExist:
        raise Http404
    products = Product.custom_objects.all().filter(category=category)
    context = {
        'category': category,
        'products': products,
        'cart': cart,
        'products_list': products_list,
    }
    return render(request, 'store_app/products.html', context)


def show_product(request, **kwargs):
    category = Category.objects.get(slug=kwargs['category_slug'])
    product = Product.objects.get(slug=kwargs['product_slug'])
    context = {
        'category': category,
        'product': product,
    }
    return render(request, 'store_app/product.html', context)


def cart_view(request, **kwargs):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'store_app/cart.html', context)


def add_to_cart_view(request):
    cart = get_or_create_cart(request)
    slug = request.GET['product_slug']
    cart.add_to_cart(slug)
    return JsonResponse({'cart_total': cart.items.count()})


def remove_from_cart_view(request):
    cart = get_or_create_cart(request)
    slug = request.GET['product_slug']
    cart.remove_from_cart(slug)
    return JsonResponse({'cart_total': cart.items.count()})


def change_item_quantity(request):
    cart = get_or_create_cart(request)
    quantity = request.GET['quantity']
    item_id = request.GET['item_id']
    item = cart.items.get(id=int(item_id))
    item.quantity = int(quantity)
    item.item_total = int(quantity) * Decimal(item.product.price)
    item.save()
    return JsonResponse({'cart_total': cart.items.count(), 'item_total': item.item_total})
