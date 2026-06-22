from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from catalog.models import Product


def index(request: HttpRequest) -> HttpResponse:
    latest_products = Product.objects.order_by('-created_at')[:5]
    print(latest_products)  # вывод в консоль сервера
    return render(request, "index.html", {"products": latest_products})


def contacts(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("name")
        messages.success(request, f"Спасибо, {name}! Мы свяжемся с вами.")
        return redirect("catalog:contacts")
    return render(request, "contacts.html")
