FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install poetry && poetry install --no-dev

COPY src/ .

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]