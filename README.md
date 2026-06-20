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



## Кодстайл

```bash
poetry run flake8 src tests          # линтер
poetry run black src tests           # форматирование
poetry run isort src tests           # сортировка импортов
poetry run mypy src                  # проверка типов
```

Или запустить все линтеры одной командой:

```bash
poetry run ./lint.sh
```
