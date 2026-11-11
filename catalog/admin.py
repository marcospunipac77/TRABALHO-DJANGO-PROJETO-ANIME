from django.contrib import admin

from .models import Anime, Episode, Favorite, Genre, Season


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ["title", "release_year", "status"]
    list_filter = ["status", "release_year", "genres"]
    search_fields = ["title", "synopsis"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SeasonInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ["anime", "number", "title", "release_year"]
    list_filter = ["release_year"]
    search_fields = ["anime__title", "title"]
    inlines = [EpisodeInline]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ["title", "season", "number", "duration_minutes"]
    list_filter = ["season__anime"]
    search_fields = ["title", "season__anime__title"]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "anime", "created_at"]
    search_fields = ["user__username", "anime__title"]
