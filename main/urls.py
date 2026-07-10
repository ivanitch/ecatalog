from django.urls import path

from .views import ContactsView

app_name = 'main'

urlpatterns = [
    path("contacts/", ContactsView.as_view(), name="contacts"),
]
