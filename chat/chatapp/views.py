from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import *

# Create your views here.


def index(request):
    user = request.user.username
    msg = Message.objects.filter(receiver=user)
    new_msg = []
    for i in msg:
        if i.is_read == False:
            new_msg.append(i.sender)
    new_msg = list(dict.fromkeys(new_msg))

    return render(request, 'chatapp/start.html', {
        'new': new_msg,
        'user': user,
    })


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


# Posting of message
@csrf_exempt
def post(request, username):
    if request.method == 'POST':
        msg = request.POST['text']
        receiver = username
        sender = request.user.username
        message = Message(message=msg, sender=sender, receiver=receiver)
        message.save()
    return redirect('home')


# profile paage with all of freinds connections
def home(request):

    user = request.user.username
    friends = User.objects.all()
    users = []
    # creating an arr of users
    for u in friends:
        users.append(u.username)
    # check for the currant user and removes it from the arr
    for currant in users:
        if currant == user:
            users.remove(currant)

    return render(request, 'chatapp/home.html', {
        'user': user,
        'users': users,
    })


# function for the chat messages
def chat(request, username):

    user = request.user.username
    recived = Message.objects.filter(receiver=user)

    msg = Message.objects.filter(receiver=username)
    # combining the two query in one
    data = recived | msg

    msg_data = data.distinct().order_by('timestamp')
    readed = []
    for read in msg_data:
        if read.sender == username:
            read.is_read = True
            read.save()
            readed.append(read)
        elif read.receiver == user:
            read.is_read = True
            read.save()
            readed.append(read)

    return render(request, 'chatapp/index.html', {
        'user': user,
        'reciver': username,
        'messages': msg_data,

    })


# Api to get JSON data
def chat_api(request, username):

    context_data = serializers.serialize(
        'json', Message.objects.all())
    context = JsonResponse(context_data, safe=False)
    print(context_data)
    return HttpResponse(context_data, content_type="text/json-comment-filtered")
