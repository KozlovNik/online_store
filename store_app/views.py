from django.shortcuts import render
from store_app.models import Product, Category, Brand, Cart, CartItem
from django.http import HttpResponseRedirect, Http404
from .functions_for_views import get_or_create_cart
from django.urls import reverse


def index(request):
    print(request)
    products = Product.objects.all()
    cart = get_or_create_cart(request)
    context = {
        'products': products,
        'cart': cart,
    }
    return render(request, 'store_app/index.html', context)


def show_category(request, **kwargs):
    cart = get_or_create_cart(request)
    try:
        category = Category.objects.get(slug=kwargs['category_slug'])
    except Category.DoesNotExist:
        raise Http404
    products = Product.custom_objects.all().filter(category=category)
    context = {
        'category': category,
        'products': products,
        'cart': cart
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


def add_to_cart_view(request, slug):
    cart = get_or_create_cart(request)
    cart.add_to_cart(slug)
    return HttpResponseRedirect(reverse('cart'))


def remove_from_cart_view(request, slug):
    cart = get_or_create_cart(request)
    cart.remove_from_cart(slug)
    return HttpResponseRedirect(reverse('cart'))
