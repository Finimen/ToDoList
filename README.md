# 📝 Django Todo List Application
https://img.shields.io/badge/Django-4.2.7-green
https://img.shields.io/badge/Python-3.9+-blue
https://img.shields.io/badge/PostgreSQL-13-orange
https://img.shields.io/badge/tests-27%2520passed-brightgreen
https://img.shields.io/badge/coverage-95%2525-green

## A modern, feature-rich Todo List application built with Django featuring user authentication, priority management, and AJAX functionality.

# ✨ Features
## 🔐 Authentication & User Management
User registration and login

Secure password validation

Session-based authentication

Protected routes and user-specific data

## 📋 Todo Management
Create, read, update, and delete todos

Priority levels (Low, Medium, High)

Due dates with automatic day calculation

Mark tasks as complete/incomplete

User-specific todo lists

## 🚀 Advanced Features
AJAX-powered interface - seamless user experience

Real-time updates without page reloads

Responsive design - works on all devices

Comprehensive logging - structured application logs

Priority-based organization - visual task prioritization

## 🛡️ Quality & Reliability
Comprehensive test suite - 27+ unit and integration tests

CI/CD pipeline - automated testing on every commit

Code coverage - 95%+ test coverage

Code quality - automated formatting and linting

## 🏗️ Project Structure
```text
to_do_list/
├── src/                    # Django project source
│   ├── project/           # Project settings and configuration
│   ├── todos/             # Todo application
│   │   ├── tests/         # Comprehensive test suite
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── test_ajax.py
│   │   ├── models.py      # Todo data models
│   │   ├── views.py       # Business logic
│   │   └── forms.py       # Django forms
│   ├── accounts/          # User authentication app
│   └── manage.py
├── .github/workflows/     # CI/CD configuration
├── pyproject.toml         # Project dependencies
└── pytest.ini            # Test configuration
```
## 🚀 Quick Start
Prerequisites
Python 3.9+

PostgreSQL 13+

Poetry (for dependency management)

Installation
Clone the repository
```bash
git clone https://github.com/yourusername/to-do-list.git
cd to-do-list
```

Install dependencies
```bash
poetry install
```

Set up environment variables
```bash
export DATABASE_URL="postgresql://user:password@localhost/todo"
export SECRET_KEY="your-secret-key-here"
export DEBUG=True
```

Run database migrations
```bash
cd src
python manage.py migrate
```

Create superuser (optional)
```bash
python manage.py createsuperuser
```

Start development server
```bash
python manage.py runserver
```

Visit http://localhost:8000 to see the application.

# 🧪 Testing
The project includes a comprehensive test suite:

bash
```
# Run all tests
pytest src/todos/tests/ -v


# Run with coverage report

pytest src/todos/tests/ --cov=todos --cov-report=html

# Run specific test categories
pytest src/todos/tests/test_models.py -v    # Model tests
pytest src/todos/tests/test_views.py -v     # View tests  
pytest src/todos/tests/test_ajax.py -v      # AJAX integration tests
```

## Test Coverage
Models: 100% coverage

Views: 95% coverage

AJAX functionality: 90% coverage

Authentication: 100% coverage

# 🛠️ Development
Code Quality
```bash
# Format code
black src/

# Check code style
black --check src/

# Run linting
flake8 src/
Database Management
bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```
# 🔧 Configuration
Environment Variables
Variable	Description	Default
DATABASE_URL	PostgreSQL connection string	postgresql://postgres:mysecretpassword@localhost/todo
SECRET_KEY	Django secret key	secret-key
DEBUG	Debug mode	True
ALLOWED_HOSTS	Allowed hosts	localhost,127.0.0.1
Database Configuration
The application uses PostgreSQL with the following default settings:

Database: todo

User: postgres

Password: mysecretpassword

Host: localhost

Port: 5432

# 📊 API Endpoints
Todo Endpoints
```
Method	URL	Description
GET	/todos/	List all user todos
POST	/todos/	Create new todo (supports AJAX)
GET	/todos/<id>/	Get todo details
POST	/todos/<id>/	Update todo (supports AJAX)
DELETE	/todos/<id>/	Delete todo (AJAX only)
POST	/todos/<id>/complete/	Mark todo as complete
POST	/todos/<id>/uncomplete/	Mark todo as incomplete
Authentication Endpoints
Method	URL	Description
GET/POST	/accounts/login/	User login
GET/POST	/accounts/logout/	User logout
GET/POST	/accounts/signup/	User registration
```
## 🤝 Contributing
We welcome contributions! Please see our Contributing Guide for details.

Development Workflow
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

Code Standards
Follow PEP 8 style guide

Write tests for new functionality

Ensure all tests pass

Update documentation as needed

## 📈 CI/CD Status
This project uses GitHub Actions for continuous integration:

Tests: Run on Python 3.9, 3.10, 3.11

Code Quality: Black formatting check

Coverage: Codecov integration

Security: Dependency scanning

https://github.com/yourusername/to-do-list/actions/workflows/ci.yml/badge.svg
https://codecov.io/gh/yourusername/to-do-list/branch/main/graph/badge.svg

## 🐛 Bug Reports
Found a bug? Please open an issue with:

Detailed description of the bug

Steps to reproduce

Expected vs actual behavior

Environment details

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

# 🙏 Acknowledgments
Django team for the excellent web framework

PostgreSQL team for the reliable database

Pytest and Factory Boy for testing tools

GitHub Actions for CI/CD infrastructure

Built with ❤️ using Django and modern development practices

<div align="center">
## 🚀 Ready to organize your tasks?
Get Started • View Demo • Report Issue

</div>
📞 Support
Documentation: View Docs

Issues: GitHub Issues

Email: finimensniper@gmail.com
