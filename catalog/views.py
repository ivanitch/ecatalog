from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from catalog.models import Product, Category


def index(request: HttpRequest) -> HttpResponse:
    all_products = Product.objects.all()
    paginator = Paginator(all_products, settings.PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"products": page_obj})


def contacts(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("name")
        messages.success(request, f"Спасибо, {name}! Мы свяжемся с вами.")
        return redirect("catalog:contacts")
    return render(request, "contacts.html")


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def product_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        if name and price:
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
            )
            messages.success(request, "Товар успешно добавлен!")
            return redirect("catalog:home")
        else:
            messages.error(request, "Заполните обязательные поля.")
    return render(request, "product_create.html")


"""CBV для Категорий"""


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
