from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from catalog.forms import ProductForm
from catalog.models import Product, Category
from catalog.services import ProductService


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


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        return ProductService.get_product_from_cache(self.kwargs.get('pk'))


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = reverse_lazy("catalog:home")
    success_message = "Товар «%(name)s» успешно добавлен!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_message = "Товар «%(name)s» успешно обновлён!"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if (obj.owner != user
                and not user.is_superuser
                and not user.has_perm('catalog.change_product')
                and not user.has_perm('catalog.can_change_product_description')):
            raise PermissionDenied("У вас нет прав для редактирования этого товара.")
        return obj

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("У вас нет прав для удаления этого товара.")
        return obj


"""Категории"""


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category/category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductService.get_products_for_category(self.object.pk)
        return context


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    permission_required = 'catalog.add_category'
    success_url = reverse_lazy('catalog:category_list')
    success_message = "Категория %(name)s успешно создана!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category/category_form.html'
    permission_required = 'catalog.change_category'
    success_url = reverse_lazy('catalog:category_list')
    success_message = "Категория %(name)s успешно обновлена!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    permission_required = 'catalog.delete_category'
    success_url = reverse_lazy('catalog:category_list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.warning(request, f"Категория {category.name} была удалена.")
        return super().delete(request, *args, **kwargs)
