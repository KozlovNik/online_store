from .models import Cart
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def get_or_create_cart(request):
    try:
        cart = Cart.objects.get(id=request.session['cart_id'])
    except (Cart.DoesNotExist, KeyError):
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
    return cart


def signup_authenticated_user(request):
    if not request.user.is_authenticated and request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(request.path_info)
