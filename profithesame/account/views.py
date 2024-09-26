from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request:HttpRequest):
    return render(
        request,
        'account/dashboard.html',
        {
            'section': 'dashboard',
        }
    )

def user_logout(request:HttpRequest):
    logout(request)

    return render(
        request,
        'registration/logged_out.html',
        {}
    )
