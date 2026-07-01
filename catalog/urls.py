from django.urls import path

from . import views
from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView
)

app_name = "catalog"

urlpatterns = [
    path("", views.index, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/create/", views.product_create, name="product_create"),

    # Category CRUD
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
]
