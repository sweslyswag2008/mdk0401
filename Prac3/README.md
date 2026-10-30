# ПР3 — Установка окружения и каркас проекта («Библиотека»)

Django-проект «Библиотека» (система учёта книг): кастомный пользователь с ролями
и справочники (Места хранения, Разделы, Издательства, Издания).

## Запуск (Windows, VS Code)

1. Создать и активировать окружение:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Установить зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Поднять PostgreSQL (БД/пользователь `biblioteka`) и Redis (Memurai) — см. задание ПР3,
   либо использовать значения из `.env`.
4. Применить миграции и создать администратора:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Запустить сервер:
   ```
   python manage.py runserver
   ```
6. Открыть админку: http://127.0.0.1:8000/admin/
