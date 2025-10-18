import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from todos.models import ToDo
from datetime import timedelta
import factory
from unittest.mock import patch


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')


class ToDoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ToDo

    title = factory.Sequence(lambda n: f'Test Todo {n}')
    content = "Test content"
    user = factory.SubFactory(UserFactory)
    priority = 'medium'


@pytest.mark.django_db
class TestToDoModel:
    
    def test_todo_creation(self):
        todo = ToDoFactory()
        assert todo.title.startswith('Test Todo')
        assert todo.user is not None
        assert todo.completed is False
        assert todo.priority == 'medium'
        assert todo.created_at is not None

    def test_todo_ordering(self):
        user = UserFactory()
        todo1 = ToDoFactory(user=user, title="First")
        todo2 = ToDoFactory(user=user, title="Second")

        todos = ToDo.objects.filter(user=user)

        # ИСПРАВЛЕНО: Поскольку ordering = ['-created_at'], 
        # последний созданный элемент (todo2) должен быть ПЕРВЫМ в списке
        assert todos[0] == todo2  # Последний созданный
        assert todos[1] == todo1  # Первый созданный

    def test_days_until_due_future(self):
        """Тест расчета дней до дедлайна (будущая дата) с mock"""
        fixed_now = timezone.now()
        future_date = fixed_now + timedelta(days=5)
        
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = fixed_now
            todo = ToDoFactory(due_date=future_date)
            assert todo.days_until_due == 5

    def test_days_until_due_past(self):
        """Тест расчета дней до дедлайна (прошедшая дата) с mock"""
        fixed_now = timezone.now()
        past_date = fixed_now - timedelta(days=3)
        
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = fixed_now
            todo = ToDoFactory(due_date=past_date)
            assert todo.days_until_due == -3

    def test_days_until_due_none(self):
        todo = ToDoFactory(due_date=None)
        assert todo.days_until_due is None

    def test_priority_choices(self):
        valid_priorities = ['low', 'medium', 'high']
        
        for priority in valid_priorities:
            todo = ToDoFactory(priority=priority)
            assert todo.priority == priority

    def test_title_max_length(self):
        todo = ToDoFactory(title="A" * 150)
        todo.full_clean()

    def test_title_too_long(self):
        user = UserFactory()
        todo = ToDo(
            title="A" * 151,
            content="Test content",
            user=user,
            priority='medium'
        )
        
        with pytest.raises(ValidationError):
            todo.full_clean()

    @pytest.mark.parametrize("priority,expected", [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    def test_priority_display(self, priority, expected):
        todo = ToDoFactory(priority=priority)
        assert todo.get_priority_display() == expected