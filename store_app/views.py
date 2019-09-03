from django.shortcuts import render
from store_app.models import Product, Category, Brand


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'store_app/index.html', context)


def show_category(request, **kwargs):
    category = Category.objects.get(slug=kwargs['category_slug'])
    products = Product.custom_objects.all().filter(category=category)
    context = {
        'category': category,
        'products': products,
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
