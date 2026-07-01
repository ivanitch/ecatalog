# ECatalog

Учебный проект по созданию системы управления каталогом товаров на Python, разработанный в рамках курса
«Python-разработчик с нуля» от онлайн-университета Skypro.

---

## Установка и запуск

```bash
# Установка зависимостей
poetry install

# Применение миграций
poetry run python manage.py migrate

# Запуск сервера разработки
poetry run python manage.py runserver
```

## Миграции

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Админка

Создание суперпользователя (логин/пароль по умолчанию: `admin` / `admin`):

```bash
poetry run python manage.py createsuperuser
```

Панель доступна по адресу: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Django Shell

```bash
poetry run python manage.py shell -i ipython
```

Примеры запросов в shell:

```python
from catalog.models import Category, Product

# Создание категорий и продуктов
cat = Category.objects.create(name='Электроника', description='Гаджеты')
Product.objects.create(name='Телефон', price=29999, category=cat)

# Получение данных
Category.objects.all()
Product.objects.all()
Product.objects.filter(category=cat)

# Обновление и удаление
p = Product.objects.get(name='Телефон')
p.price = 25999
p.save()
p.delete()
```

## Блог

Раздел для SEO - статьи с превью-изображением, счётчиком просмотров и признаком публикации.
На главной странице списка отображаются только опубликованные статьи; счётчик просмотров
увеличивается при открытии статьи. При достижении статьёй 100 просмотров на почту
(`DEFAULT_FROM_EMAIL` в `.env`) отправляется уведомление.

Доступен по адресу: [http://127.0.0.1:8000/blogs/](http://127.0.0.1:8000/blogs/)

Для отправки писем в режиме разработки используется консольный backend
(`EMAIL_BACKEND = django.core.mail.backends.console.EmailBackend`) — письма выводятся в консоль
сервера, а не отправляются по-настоящему.

## Фикстуры

Экспорт данных из БД:

```bash
poetry run python manage.py dumpdata catalog.Category --indent 4 > catalog/fixtures/categories.json
poetry run python manage.py dumpdata catalog.Product --indent 4 > catalog/fixtures/products.json
poetry run python manage.py dumpdata blog.BlogPost --indent 4 > blog/fixtures/blog_posts.json
```

Загрузка фикстур в БД:

```bash
poetry run python manage.py loaddata catalog/fixtures/categories.json
poetry run python manage.py loaddata catalog/fixtures/products.json
poetry run python manage.py loaddata blog/fixtures/blog_posts.json
```

## Кастомная команда: заполнение БД

Очищает все существующие данные и загружает тестовые продукты и категории:

```bash
poetry run python manage.py fill_db
```
