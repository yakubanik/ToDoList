from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import CreateTodoForm


def index(request):
    return render(request, 'todo/index.html', {'user': request.user})


def current_todos(request):
    todos_list = Todo.objects.filter(author_id=request.user, completed__isnull=True).order_by('-edited')
    return render(request, 'todo/view_todos.html', {'todos': todos_list})


def completed_todos(request):
    todos_list = Todo.objects.filter(author_id=request.user, completed__isnull=False).order_by('-edited')
    return render(request, 'todo/completed_todos.html', {'todos': todos_list})


def view_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author_id=request.user)
    return render(request, 'todo/view_todo.html', {'todo': todo})


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': CreateTodoForm})
    else:
        try:
            form = CreateTodoForm(request.POST)
            new_model = form.save(commit=False)
            new_model.user = request.user
            new_model.save()
            return redirect('todos')
        except ValueError:
            return render(request, 'todo/view_todos.html', {'form': CreateTodoForm,
                                                            'error_message': 'Invalid value entered'})


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


def sign_out(request):
    logout(request)
    return redirect('index')
