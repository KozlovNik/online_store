from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            messages.success(request, 'Аккаунт {} был успешно создан'.format(email))
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form': form})
