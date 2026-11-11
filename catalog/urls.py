from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.AnimeListView.as_view(), name="home"),
    path("favoritos/", views.favorite_list, name="favorites"),
    path("anime/novo/", views.AnimeCreateView.as_view(), name="anime_create"),
    path("anime/<slug:slug>/", views.AnimeDetailView.as_view(), name="anime_detail"),
    path("anime/<slug:slug>/editar/", views.AnimeUpdateView.as_view(), name="anime_edit"),
    path("anime/<slug:slug>/favorito/", views.toggle_favorite, name="toggle_favorite"),
]
