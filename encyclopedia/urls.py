from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_results, name="search_results"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage", views.editpage, name="editpage"),
    path("<str:name>", views.title, name="title")
    ]
