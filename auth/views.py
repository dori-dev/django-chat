"""chat authentication
"""
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def register_view(request):
    """register view"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect("index")

    else:
        form = UserCreationForm()
    arg = {
        "form": form,
    }
    return render(request, "auth/register.html", arg)


def login_view(request):
    """login view"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect("index")
    else:
        form = AuthenticationForm()
    arg = {
        "form": form,
    }
    return render(request, "auth/login.html", arg)


def logout_view(request):
    """logout view"""
    if request.method == "POST":
        logout(request)
        return redirect("index")
