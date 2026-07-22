from django.urls import path

from .views import ContactsView, TestView

app_name = 'main'

urlpatterns = [
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("test/", TestView.as_view(), name="test"),
]
