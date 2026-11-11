from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField("nome", max_length=60, unique=True)
    description = models.CharField("descricao", max_length=180, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "genero"
        verbose_name_plural = "generos"

    def __str__(self):
        return self.name


class Anime(models.Model):
    class Status(models.TextChoices):
        AIRING = "airing", "Em exibicao"
        COMPLETED = "completed", "Completo"
        UPCOMING = "upcoming", "Em breve"

    title = models.CharField("titulo", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    synopsis = models.TextField("sinopse")
    release_year = models.PositiveSmallIntegerField("ano de lancamento")
    status = models.CharField(
        "status", max_length=12, choices=Status.choices, default=Status.COMPLETED
    )
    poster_url = models.URLField("URL do poster", blank=True)
    genres = models.ManyToManyField(Genre, related_name="animes", verbose_name="generos")
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "anime"
        verbose_name_plural = "animes"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "anime"
            candidate = base_slug
            suffix = 2
            while Anime.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:anime_detail", kwargs={"slug": self.slug})


class Season(models.Model):
    anime = models.ForeignKey(
        Anime, on_delete=models.CASCADE, related_name="seasons", verbose_name="anime"
    )
    number = models.PositiveSmallIntegerField("numero da temporada")
    title = models.CharField("titulo", max_length=120, blank=True)
    release_year = models.PositiveSmallIntegerField("ano", null=True, blank=True)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(fields=["anime", "number"], name="unique_anime_season")
        ]
        verbose_name = "temporada"
        verbose_name_plural = "temporadas"

    def __str__(self):
        return self.title or f"Temporada {self.number} - {self.anime.title}"


class Episode(models.Model):
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="episodes", verbose_name="temporada"
    )
    number = models.PositiveSmallIntegerField("numero do episodio")
    title = models.CharField("titulo", max_length=160)
    synopsis = models.TextField("sinopse", blank=True)
    duration_minutes = models.PositiveSmallIntegerField("duracao (minutos)", default=24)
    video_url = models.URLField("link do trailer/video", blank=True)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(fields=["season", "number"], name="unique_season_episode")
        ]
        verbose_name = "episodio"
        verbose_name_plural = "episodios"

    def __str__(self):
        return f"{self.number}. {self.title}"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="anime_favorites",
        verbose_name="usuario",
    )
    anime = models.ForeignKey(
        Anime, on_delete=models.CASCADE, related_name="favorited_by", verbose_name="anime"
    )
    created_at = models.DateTimeField("adicionado em", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "anime"], name="unique_user_anime_favorite")
        ]
        verbose_name = "favorito"
        verbose_name_plural = "favoritos"

    def __str__(self):
        return f"{self.user} - {self.anime}"
