from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def home(request):
    # return render(request, 'UserHandling/home.html')
    return redirect('main-orders')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.add_message(request, messages.SUCCESS, f'Pomyślnie zarejestrowano użytkownika {username}.')
            return redirect('user-login')
    else:
        form = UserCreationForm()

    return render(request, 'UserHandling/register.html', {'form': form })
