from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import ContactForm


class ContactsView(SuccessMessageMixin, View):
    """Страница контактов"""

    @staticmethod
    def get(request):
        form = ContactForm()
        return render(request, "contacts.html", {"form": form})

    @staticmethod
    def post(request):
        form = ContactForm(request.POST)

        if form.is_valid():
            # Данные формы валидны
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            message = form.cleaned_data.get('message')

            # Здесь можно отправить письмо, сохранить в БД и т.д.
            # Например:
            # send_email(name, phone, message)

            success_message = "Спасибо, %(name)s! Мы свяжемся с вами." if phone else "Спасибо, %(name)s!"
            success_url = reverse_lazy("main:contacts")

            messages.success(request, success_message % {'name': name})

            return redirect(success_url)
        else:
            # Если форма невалидна, показываем ошибки
            return render(request, "contacts.html", {'form': form})


class TestView(View):
    @staticmethod
    def get(request):
        from django.core.cache import cache
        from django.http import HttpResponse
        data = cache.get('test')
        if not data:
            data = {
                'name': 'John',
                'age': 25,
            }
            cache.set('test', data, 60 * 15)
        return render(request, "test.html", {"data": data})



