from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, get_list_or_404, redirect
from .models import Todo


def index(request):
    return render(request, 'todo/index.html', {'user': request.user})


def view_todos(request):
    todos = get_list_or_404(Todo)
    return render(request, 'todo/view_todos.html', {'todos': todos})


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'todo/sign_up.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                username = request.POST['username']
                password = request.POST['password1']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'todo/sign_up.html', {'form': UserCreationForm,
                                                             'error_message': 'Login is already taken'})
        else:
            return render(request, 'todo/sign_up.html', {'form': UserCreationForm,
                                                         'error_message': 'Passwords do not match'})


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'todo/sign_in.html', {'form': AuthenticationForm})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'todo/sign_in.html', {'form': AuthenticationForm,
                                                         'error_message': 'Incorrect username and/or password'})
        else:
            login(request, user)
            return redirect('index')
