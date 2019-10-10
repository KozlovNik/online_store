from django.shortcuts import render, HttpResponseRedirect
from store_app.models import Product, Category
from django.http import Http404, JsonResponse
from .functions_for_views import get_or_create_cart, signup_authenticated_user
from decimal import Decimal
from .forms import UserLoginForm
from django.contrib.auth import authenticate, logout
from django.core.paginator import Paginator
from .forms import OrderForm, RegisteredUserOrderForm


def index(request):
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    products = Product.objects.all()
    cart = get_or_create_cart(request)
    products_list = cart.get_product_items()
    context = {
        'products': products,
        'cart': cart,
        'products_list': products_list,
        'login_form': login_form,
    }
    return render(request, 'store_app/index.html', context)


def show_category(request, **kwargs):
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    cart = get_or_create_cart(request)
    products_list = cart.get_product_items()
    try:
        category = Category.objects.get(slug=kwargs['category_slug'])
    except Category.DoesNotExist:
        raise Http404
    products = Product.custom_objects.all().filter(category=category)
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products_object = paginator.get_page(page)
    context = {
        'category': category,
        'products': products_object,
        'cart': cart,
        'products_list': products_list,
        'login_form': login_form,
    }
    return render(request, 'store_app/products.html', context)


def show_catalog(request, **kwargs):
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    cart = get_or_create_cart(request)
    products = Product.objects.all()
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products_object = paginator.get_page(page)
    categories = Category.objects.all()
    products_list = cart.get_product_items()
    context = {
        'categories': categories,
        'products': products_object,
        'cart': cart,
        'login_form': login_form,
        'products_list': products_list,
    }
    return render(request, 'store_app/catalog.html', context)


def show_product(request, **kwargs):
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    category = Category.objects.get(slug=kwargs['category_slug'])
    product = Product.objects.get(slug=kwargs['product_slug'])
    context = {
        'category': category,
        'product': product,
        'login_form': login_form,
    }
    return render(request, 'store_app/product.html', context)


def cart_view(request, **kwargs):
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    cart = get_or_create_cart(request)
    if request.method == 'POST' and 'checkout' in request.POST:
        if request.user.is_authenticated:
            order_form = RegisteredUserOrderForm(request.POST)
        else:
            order_form = OrderForm(request.POST)
        if order_form.is_valid():
            if request.user.is_authenticated:
                obj = order_form.save(commit=False)
                obj.user = request.user
                obj.first_name = request.user.first_name
                obj.last_name = request.user.last_name
            else:
                obj = order_form.save(commit=False)
            obj.cart = cart
            obj.status = 'Принят в обработку'
            obj.save()
            del request.session['cart_id']
            return HttpResponseRedirect(request.path_info)

    if request.user.is_authenticated:
        order_form = RegisteredUserOrderForm()
    else:
        order_form = OrderForm()

    context = {
        'cart': cart,
        'login_form': login_form,
        'order_form': order_form
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
    if request.is_ajax() and 'checkout' not in request.POST:
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return JsonResponse({'response': True})
            return JsonResponse({'response': False})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(request.path_info)
