from catalog.models import Category
from catalog.services import CategoryService


def footer_data(request):
    return {
        "footer_categories": CategoryService.get_categories_from_cache()
    }
