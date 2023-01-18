from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.view_todos, name='todos'),
    path('<int:todo_id>/', views.todo_by_id, name='view_todo'),
    path('create_todo/', views.create_todo, name='create_todo'),
    path('todos/completed/', views.completed_todos, name='completed_todos'),

    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
]
