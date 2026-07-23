from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = "catalog"
    verbose_name = "Каталог"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import catalog.signals
