from django.conf import settings
from django.core.cache import cache
from catalog.models import Product, Category


class ProductService:
    @staticmethod
    def get_product_from_cache(product_id):
        if not settings.CACHE_ENABLED:
            return Product.objects.get(pk=product_id)
        key = f'product_detail_{product_id}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(pk=product_id)
            cache.set(key, product, settings.CACHE_TTL)

        return product

    @staticmethod
    def get_products_for_category(category_id):
        if not settings.CACHE_ENABLED:
            return Product.objects.filter(category_id=category_id)

        key = f'category_{category_id}'
        products = cache.get(key)

        if products is None:
            products = list(Product.objects.filter(category_id=category_id))
            cache.set(key, products, settings.CACHE_TTL)

        return products
