from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Todo
from .forms import TodoCreateForm


def index(request):
    if request.user.is_authenticated:
        return redirect('current_todos')
    return render(request, 'todo/index.html', {'user': request.user})


@login_required(login_url='sign_in')
def current_todos(request):
    todos_list = Todo.objects.filter(author_id=request.user, completed__isnull=True).order_by('-edited')
    return render(request, 'todo/view_todos.html', {'todos': todos_list})


@login_required(login_url='sign_in')
def completed_todos(request):
    todos_list = Todo.objects.filter(author_id=request.user, completed__isnull=False).order_by('-edited')
    return render(request, 'todo/completed_todos.html', {'todos': todos_list})


@login_required(login_url='sign_in')
def view_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author_id=request.user)
    return render(request, 'todo/view_todo.html', {'todo': todo})


@login_required(login_url='sign_in')
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/input_todo.html', {'form': TodoCreateForm()})
    else:
        form = TodoCreateForm(request.POST)
        try:
            new_todo = form.save(commit=False)
            new_todo.author = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/input_todo.html',
                          {'form': TodoCreateForm(), 'error_message': 'Bad data passed in. Try again.'})


@login_required(login_url='sign_in')
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author_id=request.user)
    if request.method == 'GET':
        form = TodoCreateForm(instance=todo)
        return render(request, 'todo/input_todo.html', {'todo': todo, 'form': form})
    else:
        form = TodoCreateForm(request.POST, instance=todo)
        try:
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/input_todo.html',
                          {'todo': todo, 'form': form, 'error_message': 'Bad data passed in. Try again.'})


@login_required(login_url='sign_in')
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author_id=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required(login_url='sign_in')
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author_id=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')


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


@login_required(login_url='sign_in')
def sign_out(request):
    logout(request)
    return redirect('index')
