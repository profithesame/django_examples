from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import LoginForm


def user_login(request:HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else: 
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})
