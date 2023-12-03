from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse

from user.forms import RegisterForm


def home(request: HttpRequest) -> HttpResponse:
    """Обрабатывает запрос на домашнюю страницу."""
    return render(request, 'user/home.html')


def sign_up(request: HttpRequest) -> HttpResponse:
    """Обрабатывает регистрацию нового пользователя."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})
