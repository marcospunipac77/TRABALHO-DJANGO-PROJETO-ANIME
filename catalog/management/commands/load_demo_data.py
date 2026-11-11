from django.core.management.base import BaseCommand

from catalog.models import Anime, Episode, Genre, Season


class Command(BaseCommand):
    help = "Carrega dados ficticios para demonstrar o catalogo."

    def handle(self, *args, **options):
        genres = {
            name: Genre.objects.get_or_create(name=name)[0]
            for name in ["Aventura", "Fantasia", "Ficcao cientifica"]
        }
        demo_animes = [
            {
                "slug": "a-lenda-de-aster",
                "title": "A Lenda de Aster",
                "synopsis": (
                    "Em um arquipelago flutuante, uma aprendiz de cartografa busca "
                    "as ilhas que desapareceram dos mapas."
                ),
                "release_year": 2025,
                "status": Anime.Status.COMPLETED,
                "genres": ["Aventura", "Fantasia"],
                "season_title": "A Ilha que Sumiu",
                "episodes": ["O mapa incompleto", "Acima das nuvens", "Aster desperta"],
            },
            {
                "slug": "ceu-de-neon",
                "title": "Céu de Néon",
                "synopsis": (
                    "Uma equipe de jovens inventores tenta restaurar a energia "
                    "de uma cidade que nunca mais viu o amanhecer."
                ),
                "release_year": 2026,
                "status": Anime.Status.AIRING,
                "genres": ["Ficcao cientifica", "Aventura"],
                "season_title": "A Cidade Adormecida",
                "episodes": ["Sinais na chuva", "O trem suspenso", "Uma nova luz"],
            },
            {
                "slug": "viajantes-do-vento",
                "title": "Viajantes do Vento",
                "synopsis": (
                    "Dois amigos partem em uma jornada por terras fantásticas "
                    "para encontrar a origem de uma melodia misteriosa."
                ),
                "release_year": 2024,
                "status": Anime.Status.COMPLETED,
                "genres": ["Fantasia", "Aventura"],
                "season_title": "A Melodia Distante",
                "episodes": ["A primeira nota", "O vale silencioso", "Canção de chegada"],
            },
        ]

        for item in demo_animes:
            anime, _ = Anime.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "synopsis": item["synopsis"],
                    "release_year": item["release_year"],
                    "status": item["status"],
                },
            )
            anime.genres.set(genres[name] for name in item["genres"])
            season, _ = Season.objects.update_or_create(
                anime=anime,
                number=1,
                defaults={"title": item["season_title"], "release_year": item["release_year"]},
            )
            for number, title in enumerate(item["episodes"], start=1):
                Episode.objects.update_or_create(
                    season=season,
                    number=number,
                    defaults={
                        "title": title,
                        "synopsis": "Episodio demonstrativo original.",
                        "duration_minutes": 24,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Dados ficticios carregados com sucesso."))
