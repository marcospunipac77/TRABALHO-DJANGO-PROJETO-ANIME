from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Anime, Episode, Favorite, Genre, Season


class CatalogTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Aventura")
        self.anime = Anime.objects.create(
            title="Jornada Estelar",
            synopsis="Uma aventura pelo universo.",
            release_year=2025,
        )
        self.anime.genres.add(self.genre)
        self.season = Season.objects.create(anime=self.anime, number=1)
        self.episode = Episode.objects.create(
            season=self.season, number=1, title="O primeiro passo"
        )

    def test_related_catalog_data_and_unique_slugs(self):
        second_anime = Anime.objects.create(
            title=self.anime.title,
            synopsis="Outra historia.",
            release_year=2024,
        )
        self.assertNotEqual(self.anime.slug, second_anime.slug)
        self.assertEqual(self.episode.season.anime, self.anime)
        self.assertEqual(list(self.anime.genres.all()), [self.genre])

    def test_home_lists_and_filters_animes(self):
        response = self.client.get(reverse("catalog:home"), {"q": "Jornada", "genero": self.genre.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.anime.title)
        self.assertEqual(list(response.context["animes"]), [self.anime])

    def test_anime_detail_includes_seasons_and_episodes(self):
        response = self.client.get(self.anime.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Temporada 1")
        self.assertContains(response, self.episode.title)
        self.assertContains(response, "Assistir")
        self.assertContains(response, "Em breve!")

    def test_recently_viewed_animes_appear_on_home_in_visit_order(self):
        second_anime = Anime.objects.create(
            title="Outra aventura", synopsis="Mais uma sinopse.", release_year=2024
        )
        self.client.get(self.anime.get_absolute_url())
        self.client.get(second_anime.get_absolute_url())
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [anime.pk for anime in response.context["recent_animes"]],
            [second_anime.pk, self.anime.pk],
        )
        self.assertContains(response, "Continuar assistindo")

    def test_staff_can_create_and_edit_anime(self):
        user = get_user_model().objects.create_user(
            username="equipe", password="senha-forte-123", is_staff=True
        )
        self.client.force_login(user)
        create_response = self.client.post(
            reverse("catalog:anime_create"),
            {
                "title": "Novo anime",
                "synopsis": "Uma sinopse de teste.",
                "release_year": 2026,
                "status": Anime.Status.UPCOMING,
                "genres": [self.genre.pk],
            },
        )
        created = Anime.objects.get(title="Novo anime")
        self.assertRedirects(create_response, created.get_absolute_url())
        edit_response = self.client.post(
            reverse("catalog:anime_edit", kwargs={"slug": created.slug}),
            {
                "title": "Anime atualizado",
                "synopsis": "Sinopse atualizada.",
                "release_year": 2026,
                "status": Anime.Status.COMPLETED,
                "genres": [self.genre.pk],
            },
        )
        created.refresh_from_db()
        self.assertRedirects(edit_response, created.get_absolute_url())
        self.assertEqual(created.title, "Anime atualizado")

    def test_only_authenticated_users_can_toggle_favorites(self):
        url = reverse("catalog:toggle_favorite", kwargs={"slug": self.anime.slug})
        response = self.client.post(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")
        user = get_user_model().objects.create_user(username="fã", password="senha-forte-123")
        self.client.force_login(user)
        self.client.post(url)
        self.assertTrue(Favorite.objects.filter(user=user, anime=self.anime).exists())
        self.client.post(url)
        self.assertFalse(Favorite.objects.filter(user=user, anime=self.anime).exists())

    def test_anime_management_requires_staff_access(self):
        response = self.client.get(reverse("catalog:anime_create"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('catalog:anime_create')}"
        )

    def test_user_can_register_and_view_favorites(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "novo_usuario",
                "password1": "UmaSenhaForte123!",
                "password2": "UmaSenhaForte123!",
            },
        )
        self.assertRedirects(response, reverse("catalog:home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        favorites_response = self.client.get(reverse("catalog:favorites"))
        self.assertEqual(favorites_response.status_code, 200)

    def test_demo_data_command_is_repeatable(self):
        call_command("load_demo_data", stdout=None)
        call_command("load_demo_data", stdout=None)
        self.assertEqual(Anime.objects.filter(slug="a-lenda-de-aster").count(), 1)
        self.assertEqual(Anime.objects.filter(slug="attack-on-titan").count(), 1)
        self.assertEqual(
            Anime.objects.get(slug="a-lenda-de-aster").seasons.get(number=1).episodes.count(), 3
        )
