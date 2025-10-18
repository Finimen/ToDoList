#!/bin/bash

echo "=== Running Django Tests ==="

# Установка в editable mode
pip install -e .
pip install pytest pytest-django pytest-cov factory-boy black

# Запуск тестов
cd src
export DJANGO_SETTINGS_MODULE=project.settings
export SECRET_KEY="test-secret-key"
export DEBUG=False

echo "=== Running pytest ==="
pytest todos/tests/ -v --cov=todos

echo "=== Running Django checks ==="
python manage.py check

echo "=== Formatting check ==="
black --check .

echo "=== Tests Completed ==="