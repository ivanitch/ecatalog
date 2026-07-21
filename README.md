Ниже актуализированный **README.md** с учётом всех изменений: кастомной модели пользователя (вход по **Email**),
разграничения прав доступа для товаров и блога, а также обновлённых URL-адресов.

---

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

## Пользователи и Авторизация

В проекте переопределена стандартная модель пользователя (`AUTH_USER_MODEL = 'users.User'`).

* Поле `username` отключено, уникальным идентификатором для входа служит **Email**.
* Добавлены дополнительные поля: `avatar`, `phone`, `country`.
* При успешной регистрации пользователю отправляется приветственное письмо на указанный Email.

## Админка

Создание суперпользователя (вместо username запрашивается Email):

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
from users.models import User

# Создание категорий и продуктов
cat = Category.objects.create(name='Электроника', description='Гаджеты')
user = User.objects.first()
Product.objects.create(name='Телефон', price=29999, category=cat, owner=user)

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

## Каталог товаров и Права доступа

Реализован полный CRUD для товаров (создание, просмотр, редактирование, удаление) через `django.forms.ModelForm`.

### Валидация формы (`catalog/forms.py`):

* **Запрещённые слова** — название и описание товара не могут содержать слова из списка `FORBIDDEN_WORDS` (казино,
  биржа, обман, криптовалюта, дешево, полиция, крипта, бесплатно, радар), проверка регистронезависимая.
* **Цена** — не может быть отрицательной.
* **Изображение** — принимаются только файлы форматов JPEG и PNG размером не более 5 МБ.

### Разграничение прав доступа:

* Каждый создаваемый товар привязывается к автору через поле `owner`.
* Редактировать и удалять товар может только его **владелец** (`owner`), **суперпользователь**, либо пользователи с
  соответствующими правами модератора (`catalog.change_product` / `can_change_product_description`).
* Неавторизованные пользователи могут только просматривать каталог и детальную карточку товара.

## Блог

Раздел для SEO — статьи с превью-изображением, счётчиком просмотров и признаком публикации.

* В списке для обычных пользователей отображаются только опубликованные статьи (`is_published=True`).
* Счётчик просмотров увеличивается при каждом открытии статьи. При достижении 100 просмотров отправляется уведомление на
  почту (`DEFAULT_FROM_EMAIL`).
* **Права доступа**: Создание, редактирование и удаление статей ограничено — доступно только персоналу (`is_staff=True`)
  и суперпользователям.

Доступен по адресу: [http://127.0.0.1:8000/blog/](https://www.google.com/search?q=http://127.0.0.1:8000/blog/)

Для отправки писем в режиме разработки используется консольный
backend (`EMAIL_BACKEND = django.core.mail.backends.console.EmailBackend`) — письма выводятся в консоль сервера.

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
