```
myproject/                    # 🎯 Корень проекта (любое имя)
├── manage.py                 # ✅ Точка входа для команд
├── myproject/                # 🎯 Пакет проекта (то же имя)
│   ├── __init__.py
│   ├── settings.py           # ✅ Настройки проекта
│   ├── urls.py               # ✅ Главный роутинг
│   ├── asgi.py
│   └── wsgi.py
├── accounts/                 # ✅ Приложение "Аккаунты"
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py              
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── todos/                    # ✅ Приложение "Задачи"  
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py             
    ├── models.py
    ├── urls.py
    └── views.py
```
    manage - замена main
    settings - замена config
    urls - routing
    models - замена 
    views - замена handlers
    froms - замена pydantic models



    User нажимает "Submit"
    ↓
    Form.is_valid() → True
    ↓
    form.save() → UserCreationForm.save() → User.objects.create_user()
    ↓
    SQL: INSERT INTO auth_user (...) VALUES (...)
    ↓
    Запись в БД