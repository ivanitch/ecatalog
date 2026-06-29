from catalog.models import Category


def footer_data(request):
    return {
        "footer_categories": Category.objects.all()
    }
