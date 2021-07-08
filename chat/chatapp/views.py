from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        user = request.user.username

        return render(request, 'chatapp/index.html', {
            'user': user
        })
    else:
        return render(request, 'chatapp/start.html', {})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
        # if not logged in the register
    else:
        if request.method == "POST":
            form = registrationForm(request.POST or None)
            # Check if form is valid
            if form.is_valid():
                user = form.save()

                # Get user password
                raw_password = form.cleaned_data.get('password1')

                # authenticate user
                user = authenticate(username=user.username,
                                    password=raw_password)
                # login user
                login(request, user)
                return redirect('index')
        else:
            form = registrationForm()
        return render(request, 'chatapp/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
        # if not logged in then log in
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            # Check credential
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'chatapp/login.html', {'error': "Your account has been desaibled."})

            else:
                return render(request, 'chatapp/login.html', {'error': 'Invalid username or password. Try Again.'})

        return render(request, 'chatapp/login.html')


# logout user
def logout_user(request):
    if request.user.is_authenticated:

        logout(request)
        return redirect('index')
    else:
        return redirect('index')
