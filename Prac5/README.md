# ПР5 — «Библиотека»: разработка модулей и интеграция

Django-проект системы учёта книг в библиотеке: 5 модулей (авторизация, книжный фонд,
читатели, выдачи, отчёты), REST API на DRF с JWT-аутентификацией и Streamlit-дашборд
для заведующего.

## Структура
- apps/accounts — авторизация (JWT: регистрация, вход, профиль), сотрудники библиотеки
- apps/catalog  — книжный фонд (авторы, книги) + CRUD API, смена статуса книги
- apps/readers  — читатели (читательские билеты) + CRUD API
- apps/loans    — выдачи (на дом / в читальный зал / бронь), выдать, принять, отменить
- apps/reports  — отчёты (показатели, выдачи по дням, топ книг, нагрузка, фонд, должники)
- dashboard/app.py — панель заведующего на Streamlit

## Бизнес-логика
- Оформление выдачи резервирует книгу (статус «Забронирована»).
- «Выдать» → книга «Выдана», срок возврата 14 дней (для читального зала — в тот же день).
- «Принять» → книга снова «В фонде»; за каждый день просрочки штраф 5 руб.
- «Отменить» → книга возвращается в фонд.

## Запуск (Windows, VS Code)
1. Окружение и зависимости:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Поднять PostgreSQL (БД `biblioteka_db`, пользователь `biblioteka`), значения — в `.env`.
3. Миграции и администратор:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Сервер API:
   ```
   python manage.py runserver
   ```
   Админка: http://127.0.0.1:8000/admin/ , API: http://127.0.0.1:8000/api/
5. Тесты: `python manage.py test`
6. Дашборд (в отдельном терминале, в `.env` или переменных — `DASH_USER`/`DASH_PASSWORD`):
   ```
   streamlit run dashboard/app.py
   ```

## Основные API-эндпоинты
- POST /api/auth/register/ , /api/auth/login/ , GET /api/auth/me/
- /api/authors/ , /api/books/ , PATCH /api/books/{id}/status/
- /api/readers/
- /api/loans/ , POST /api/loans/{id}/issue/ , /return/ , /cancel/
- /api/reports/kpi/ , /loans/ , /top-books/ , /librarian-load/ , /stock/ , /overdue/
