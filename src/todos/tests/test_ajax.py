import pytest
import json
from django.urls import reverse
from django.contrib.auth.models import User
from todos.models import ToDo
from .test_models import UserFactory, ToDoFactory


@pytest.mark.django_db
class TestAjaxFunctionality:
    """Интеграционные тесты для AJAX-функционала"""
    
    @pytest.fixture
    def ajax_client(self, client):
        """Фикстура для клиента с AJAX headers"""
        user = UserFactory()
        client.force_login(user)
        return client

    def test_ajax_todo_creation_valid(self, ajax_client):
        """Тест AJAX создания задачи с валидными данными"""
        url = reverse('todos:todo_list')
        data = {
            'title': 'AJAX Task',
            'content': 'AJAX content',
            'priority': 'medium'
        }
        
        response = ajax_client.post(
            url, 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        
        assert response_data['success'] is True
        assert response_data['todo']['title'] == 'AJAX Task'
        assert response_data['todo']['priority'] == 'medium'
        assert ToDo.objects.filter(title='AJAX Task').exists()

    def test_ajax_todo_creation_invalid(self, ajax_client):
        """Тест AJAX создания задачи с невалидными данными"""
        url = reverse('todos:todo_list')
        data = {
            'title': '',  # Невалидно
            'content': 'AJAX content',
            'priority': 'medium'
        }
        
        response = ajax_client.post(
            url, 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        
        assert response_data['success'] is False
        assert 'errors' in response_data
        assert 'title' in response_data['errors']

    def test_ajax_todo_update_valid(self, ajax_client):
        """Тест AJAX обновления задачи с валидными данными"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user, title='Original Title')
        
        url = reverse('todos:todo_detail', args=[todo.id])
        data = {
            'title': 'Updated via AJAX',
            'content': todo.content,
            'priority': todo.priority
        }
        
        response = ajax_client.post(
            url, 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        
        assert response_data['success'] is True
        assert response_data['todo']['title'] == 'Updated via AJAX'
        
        todo.refresh_from_db()
        assert todo.title == 'Updated via AJAX'

    def test_ajax_todo_delete(self, ajax_client):
        """Тест AJAX удаления задачи"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user)
        
        url = reverse('todos:todo_detail', args=[todo.id])
        
        response = ajax_client.delete(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        
        assert response_data['success'] is True
        assert not ToDo.objects.filter(id=todo.id).exists()

    def test_ajax_todo_complete(self, ajax_client):
        """Тест AJAX отметки задачи как выполненной"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user, completed=False)
        
        url = reverse('todos:todo_complete', args=[todo.id])
        
        response = ajax_client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        
        assert response_data['success'] is True
        
        todo.refresh_from_db()
        assert todo.completed is True

    def test_ajax_todo_uncomplete(self, ajax_client):
        """Тест AJAX снятия отметки о выполнении"""
        user = User.objects.get(username__startswith='user')
        todo = ToDoFactory(user=user, completed=True)
        
        url = reverse('todos:todo_uncomplete', args=[todo.id])
        
        response = ajax_client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        
        assert response_data['success'] is True
        
        todo.refresh_from_db()
        assert todo.completed is False

    def test_mixed_ajax_and_regular_requests(self, ajax_client):
        """Тест смешанных AJAX и обычных запросов"""
        user = User.objects.get(username__startswith='user')
        
        # Создание через AJAX
        url = reverse('todos:todo_list')
        data = {'title': 'Mixed Test', 'content': 'Content', 'priority': 'low'}
        
        ajax_response = ajax_client.post(
            url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        assert ajax_response.status_code == 200
        
        # Проверка через обычный GET
        regular_response = ajax_client.get(url)
        assert regular_response.status_code == 200
        assert 'Mixed Test' in str(regular_response.content)