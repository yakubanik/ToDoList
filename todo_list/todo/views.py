from django.shortcuts import render, get_list_or_404
from .models import Todo


def index(request):
    return render(request, 'todo/index.html')


def view_todos(request):
    todos = get_list_or_404(Todo)
    return render(request, 'todo/view_todos.html', {'todos': todos})
