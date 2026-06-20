# ECatalog

Учебный проект по созданию системы управления каталогом товаров на Python, разработанный в рамках курса
«Python-разработчик с нуля» от онлайн-университета Skypro.

---

```bash
# Запуск сервера
poetry run python manage.py runserver

# Миграции
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Админка

```bash
# (admin: admin)
poetry run python manage.py createsuperuser
```

## Django shell
```bash
poetry run python manage.py shell -i ipython
```
