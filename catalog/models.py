from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Category(models.Model):
    """Сущность Категория"""
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Сущность Продукт"""
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Категория'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Владелец',
        related_name='products'
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_unpublish_product", "Разрешено снять товар с публикации"),
            ("can_change_product_description", "Разрешено изменить описание товара"),
            ("can_change_product_category", "Разрешено изменить категорию товара"),
        ]

    def __str__(self):
        return self.name


@receiver([post_save, post_delete], sender=Product)
def clear_product_category_cache(sender, instance, **kwargs):
    """
    Автоматически очищает кэш товаров категории при добавлении,
    изменении или удалении товара.
    """
    if instance.category_id:
        cache.delete(f'category_{instance.category_id}')
