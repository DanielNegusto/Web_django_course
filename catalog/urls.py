from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.contact_view, name="contacts"),
    path("catalog/", views.catalog, name="catalog"),
    path("about/", views.about, name="about")
]
