from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product


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
