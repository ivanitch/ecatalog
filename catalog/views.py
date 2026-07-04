from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from catalog.models import Product, Category


class IndexListView(ListView):
    """Каталог товаров с постраничной навигацией"""
    model = Product
    template_name = "index.html"
    context_object_name = "products"

    def get_paginate_by(self, queryset):
        return settings.PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get("is_paginated"):
            context["products"] = context["page_obj"]
        return context


class ContactsView(View):
    """Страница контактов"""

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "contacts.html")

    @staticmethod
    def post(request, *args, **kwargs):
        name = request.POST.get("name")
        messages.success(request, f"Спасибо, {name}! Мы свяжемся с вами.")
        return redirect("catalog:contacts")


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"


class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    fields = ["name", "description", "price", "image"]
    template_name = "product_create.html"
    success_url = reverse_lazy("catalog:home")
    success_message = "Товар успешно добавлен!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            if field_name != "image":
                field.widget.attrs.update({"class": "form-control"})
        return form


"""Категории"""


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category/category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category/category_detail.html'


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('catalog:category_list')
    success_message = "Категория %(name)s успешно создана!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('catalog:category_list')
    success_message = "Категория %(name)s успешно обновлена!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('catalog:category_list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.warning(request, f"Категория {category.name} была удалена.")
        return super().delete(request, *args, **kwargs)
