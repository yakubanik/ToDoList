from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from django.shortcuts import render, get_list_or_404, redirect
from .models import Todo


def index(request):
    return render(request, 'todo/index.html')


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
