from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from store_app.forms import UserLoginForm
from store_app.functions_for_views import signup_authenticated_user
from django.contrib.auth import logout
from store_app.models import Cart


def register(request):
    cart = Cart.objects.get_or_create_cart(request)
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    if request.method == 'POST' and 'register-form' in request.POST:
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            email = register_form.cleaned_data['email']
            messages.success(request, 'Аккаунт {} был успешно создан'.format(email))
            return redirect('catalog')
    else:
        register_form = UserRegisterForm()
    context = {
        'register_form': register_form,
        'cart': cart,
        'login_form': login_form
    }
    return render(request, 'users/register.html', context)


def sign_out(request):
    logout(request)
    return redirect('catalog')
