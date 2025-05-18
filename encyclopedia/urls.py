from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/search/", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("random", views.random, name="random"),
    path("edit/<str:entry>", views.edit, name="edit")
]
