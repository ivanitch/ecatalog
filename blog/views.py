from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # выводим только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])

        if obj.views_count == 100:
            send_mail(
                subject="Статья набрала 100 просмотров!",
                message=f'Поздравляем! Статья "{obj.title}" достигла 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        return obj


class BlogPostCreateView(SuccessMessageMixin, CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blogpost_form.html"
    success_message = "Статья успешно создана!"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            if field_name != "is_published":
                field.widget.attrs.update({"class": "form-control"})
        return form


class BlogPostUpdateView(SuccessMessageMixin, UpdateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blogpost_form.html"
    success_message = "Статья успешно обновлена!"

    def get_success_url(self):
        # после редактирования — на страницу этой же статьи
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            if field_name != "is_published":
                field.widget.attrs.update({"class": "form-control"})
        return form


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
