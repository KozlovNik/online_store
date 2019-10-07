from django.shortcuts import render, HttpResponseRedirect
from store_app.models import Product, Category
from django.http import Http404, JsonResponse
from .functions_for_views import get_or_create_cart, signup_authenticated_user
from decimal import Decimal
from .forms import UserLoginForm
from django.contrib.auth import authenticate, logout


def index(request):
    form = UserLoginForm()
    signup_authenticated_user(request)
    products = Product.objects.all()
    cart = get_or_create_cart(request)
    products_list = cart.get_product_items()
    context = {
        'products': products,
        'cart': cart,
        'products_list': products_list,
        'form': form,
    }
    return render(request, 'store_app/index.html', context)


def show_category(request, **kwargs):
    form = UserLoginForm()
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
        'form': form,
    }
    return render(request, 'store_app/products.html', context)


def show_product(request, **kwargs):
    form = UserLoginForm()
    category = Category.objects.get(slug=kwargs['category_slug'])
    product = Product.objects.get(slug=kwargs['product_slug'])
    context = {
        'category': category,
        'product': product,
        'form': form,
    }
    return render(request, 'store_app/product.html', context)


def cart_view(request, **kwargs):
    form = UserLoginForm()
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'store_app/cart.html', context)


def add_to_cart_view(request):
    cart = get_or_create_cart(request)
    slug = request.GET['product_slug']
    cart.add_to_cart(slug)
    cart.total_quantity = cart.get_products_quantity()
    cart_total_sum = cart.update_total_price()
    return JsonResponse({'cart_total': cart.total_quantity,
                         'cart_total_sum': cart_total_sum,
                         })


def remove_from_cart_view(request):
    cart = get_or_create_cart(request)
    slug = request.GET['product_slug']
    cart.remove_from_cart(slug)
    cart_total_price = cart.update_total_price()
    cart.total_quantity = cart.get_products_quantity()
    return JsonResponse({'cart_total': cart.total_quantity,
                         'cart_total_price': cart_total_price,
                         'cart_total_quantity': cart.total_quantity,
                         })


def change_item_quantity(request):
    cart = get_or_create_cart(request)
    quantity = request.GET['quantity']
    item_id = request.GET['item_id']
    item = cart.items.get(id=int(item_id))
    item.quantity = int(quantity)
    item.item_total = int(quantity) * Decimal(item.product.price)
    item.save()
    cart.total_quantity = cart.get_products_quantity()
    cart_total_price = cart.update_total_price()
    return JsonResponse({'item_total': item.item_total,
                         'cart_total_quantity': cart.total_quantity,
                         'cart_total_price': cart_total_price})


def authenticate_user(request):
    if request.is_ajax():
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return JsonResponse({'response': True})
            return JsonResponse({'response': False})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(request.path_info)
