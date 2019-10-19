from .forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


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
