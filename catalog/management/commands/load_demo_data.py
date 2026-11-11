from django.core.management.base import BaseCommand

from catalog.models import Anime, Episode, Genre, Season


class Command(BaseCommand):
    help = "Carrega dados ficticios para demonstrar o catalogo."

    def handle(self, *args, **options):
        genres = {
            name: Genre.objects.get_or_create(name=name)[0]
            for name in [
                "Aventura",
                "Fantasia",
                "Ficcao cientifica",
                "Acao",
                "Drama",
                "Misterio",
                "Comedia",
                "Sobrenatural",
            ]
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
            {
                "slug": "attack-on-titan",
                "title": "Attack on Titan",
                "synopsis": (
                    "Em um mundo cercado por muralhas, a humanidade luta para sobreviver "
                    "e descobrir a verdade por trás de seus misteriosos inimigos."
                ),
                "release_year": 2013,
                "status": Anime.Status.COMPLETED,
                "genres": ["Acao", "Drama", "Fantasia"],
            },
            {
                "slug": "jujutsu-kaisen",
                "title": "Jujutsu Kaisen",
                "synopsis": (
                    "Um estudante se envolve no mundo das maldições e passa a treinar "
                    "para proteger as pessoas de ameaças sobrenaturais."
                ),
                "release_year": 2020,
                "status": Anime.Status.AIRING,
                "genres": ["Acao", "Fantasia", "Sobrenatural"],
            },
            {
                "slug": "naruto",
                "title": "Naruto",
                "synopsis": (
                    "Um jovem ninja determinado busca reconhecimento enquanto aprende "
                    "sobre amizade, coragem e responsabilidade."
                ),
                "release_year": 2002,
                "status": Anime.Status.COMPLETED,
                "genres": ["Acao", "Aventura", "Fantasia"],
            },
            {
                "slug": "one-piece",
                "title": "One Piece",
                "synopsis": (
                    "Um capitão otimista reúne uma tripulação e parte pelos mares "
                    "em busca de um tesouro lendário."
                ),
                "release_year": 1999,
                "status": Anime.Status.AIRING,
                "genres": ["Acao", "Aventura", "Comedia"],
            },
            {
                "slug": "demon-slayer",
                "title": "Demon Slayer",
                "synopsis": (
                    "Após uma tragédia mudar sua família, um jovem começa uma jornada "
                    "para enfrentar criaturas perigosas e proteger quem ama."
                ),
                "release_year": 2019,
                "status": Anime.Status.COMPLETED,
                "genres": ["Acao", "Drama", "Fantasia"],
            },
            {
                "slug": "my-hero-academia",
                "title": "My Hero Academia",
                "synopsis": (
                    "Em uma sociedade de pessoas com habilidades especiais, um estudante "
                    "sonha em se tornar herói e ajudar os outros."
                ),
                "release_year": 2016,
                "status": Anime.Status.COMPLETED,
                "genres": ["Acao", "Aventura", "Drama"],
            },
            {
                "slug": "death-note",
                "title": "Death Note",
                "synopsis": (
                    "Um estudante encontra um caderno misterioso e se vê envolvido "
                    "em um jogo de inteligência que desafia a justiça."
                ),
                "release_year": 2006,
                "status": Anime.Status.COMPLETED,
                "genres": ["Drama", "Misterio", "Sobrenatural"],
            },
            {
                "slug": "spy-x-family",
                "title": "Spy x Family",
                "synopsis": (
                    "Uma família formada por pessoas com vidas secretas tenta manter "
                    "as aparências enquanto enfrenta situações inesperadas."
                ),
                "release_year": 2022,
                "status": Anime.Status.AIRING,
                "genres": ["Acao", "Comedia"],
            },
            {
                "slug": "dragon-ball-z",
                "title": "Dragon Ball Z",
                "synopsis": (
                    "Um guerreiro e seus amigos treinam e enfrentam desafios cada vez "
                    "maiores para proteger seu planeta."
                ),
                "release_year": 1989,
                "status": Anime.Status.COMPLETED,
                "genres": ["Acao", "Aventura", "Fantasia"],
            },
            {
                "slug": "solo-leveling",
                "title": "Solo Leveling",
                "synopsis": (
                    "Em um mundo de portais e caçadores, um jovem considerado fraco "
                    "recebe uma oportunidade para evoluir de forma extraordinária."
                ),
                "release_year": 2024,
                "status": Anime.Status.AIRING,
                "genres": ["Acao", "Fantasia"],
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
            item.setdefault(
                "season_title",
                "Temporada 1",
            )
            item.setdefault(
                "episodes",
                ["Episódio de demonstração 1", "Episódio de demonstração 2"],
            )
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
                        "synopsis": "Conteúdo demonstrativo do projeto.",
                        "duration_minutes": 24,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Dados ficticios carregados com sucesso."))
