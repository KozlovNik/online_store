from .models import Category
from .forms import UserLoginForm
from .functions_for_views import signup_authenticated_user
from .models import Product


def category_context(request):
    cats = Category.objects.all()
    return {
        'cats': cats,
    }


def login_form_context(request):
    login_form = UserLoginForm()
    signup_authenticated_user(request)
    return {
        'login_form': login_form
    }


def favorites_quantity_context(request):
    user_favorites_quantity = Product.custom_objects.user_favorites_quantity(request)
    return {
        'user_favorites_quantity': user_favorites_quantity,
    }
