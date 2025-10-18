from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('<int:todo_id>/', views.todo_detail, name='todo_detail'),
    path('<int:todo_id>/complete/', views.todo_complete, name='todo_complete'),
    path('<int:todo_id>/uncomplete/', views.todo_uncomplete, name='todo_uncomplete'),
]