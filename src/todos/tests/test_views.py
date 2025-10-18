import pytest
import json
from django.urls import reverse
from django.contrib.auth.models import User
from todos.models import ToDo
from todos.forms import ToDoForm
from .test_models import UserFactory, ToDoFactory


@pytest.mark.django_db
class TestToDoViews:
    """Тесты для представлений ToDo"""
    
    @pytest.fixture
    def authenticated_client(self, client):
        """Фикстура для аутентифицированного клиента"""
        user = UserFactory()
        client.force_login(user)
        return client

    @pytest.fixture
    def other_user_client(self, client):
        """Фикстура для другого пользователя"""
        user = UserFactory(username='other')
        client.force_login(user)
        return client

    def test_todo_list_GET_authenticated(self, authenticated_client):
        """Тест получения списка задач (аутентифицированный)"""
        user = User.objects.get(username__startswith='user')
        ToDoFactory.create_batch(3, user=user)
        
        url = reverse('todos:todo_list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert 'todos' in response.context
        assert len(response.context['todos']) == 3
        assert 'form' in response.context
        assert isinstance(response.context['form'], ToDoForm)

    def test_todo_list_GET_unauthenticated(self, client):
        """Тест получения списка задач (неаутентифицированный)"""
        url = reverse('todos:todo_list')
        response = client.get(url)
        
        assert response.status_code == 302  # Редирект на логин
        assert '/accounts/login/' in response.url

    def test_todo_list_POST_valid(self, authenticated_client):
        """Тест создания задачи с валидными данными"""
        url = reverse('todos:todo_list')
        data = {
            'title': 'New Task',
            'content': 'Task content',
            'priority': 'high'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == 302  # Редирект после успешного создания
        assert ToDo.objects.filter(title='New Task').exists()

    def test_todo_list_POST_invalid(self, authenticated_client):
        """Тест создания задачи с невалидными данными"""
        url = reverse('todos:todo_list')
        data = {
            'title': '',  # Пустой заголовок - невалидно
            'content': 'Task content',
            'priority': 'high'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == 200  # Остается на странице
        assert not ToDo.objects.filter(content='Task content').exists()

    def test_todo_detail_GET_owner(self, authenticated_client):
        """Тест получения деталей задачи (владелец)"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user)
        
        url = reverse('todos:todo_detail', args=[todo.id])
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert response.context['todo'] == todo

    def test_todo_detail_GET_other_user(self, authenticated_client, other_user_client):
        """Тест получения деталей задачи (чужой пользователь)"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user)
        
        url = reverse('todos:todo_detail', args=[todo.id])
        response = other_user_client.get(url)
        
        assert response.status_code == 404  # Не должен видеть чужие задачи

    def test_todo_detail_POST_valid(self, authenticated_client):
        """Тест обновления задачи с валидными данными"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user, title='Old Title')
        
        url = reverse('todos:todo_detail', args=[todo.id])
        data = {
            'title': 'Updated Title',
            'content': 'Updated content',
            'priority': 'low'
        }
        
        response = authenticated_client.post(url, data)
        todo.refresh_from_db()
        
        assert response.status_code == 302
        assert todo.title == 'Updated Title'

    def test_todo_complete(self, authenticated_client):
        """Тест отметки задачи как выполненной"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user, completed=False)
        
        url = reverse('todos:todo_complete', args=[todo.id])
        response = authenticated_client.post(url)
        todo.refresh_from_db()
        
        assert response.status_code == 302
        assert todo.completed is True

    def test_todo_uncomplete(self, authenticated_client):
        """Тест снятия отметки о выполнении"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user, completed=True)
        
        url = reverse('todos:todo_uncomplete', args=[todo.id])
        response = authenticated_client.post(url)
        todo.refresh_from_db()
        
        assert response.status_code == 302
        assert todo.completed is False