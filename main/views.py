from django.shortcuts import render
from django.views.generic import View

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
