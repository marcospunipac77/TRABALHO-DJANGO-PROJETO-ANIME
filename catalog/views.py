from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AnimeForm
from .models import Anime, Episode, Favorite, Genre


class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Sua conta foi criada.")
        return redirect("catalog:home")


class AnimeListView(ListView):
    model = Anime
    template_name = "catalog/home.html"
    context_object_name = "animes"

    def get_queryset(self):
        queryset = Anime.objects.prefetch_related("genres")
        search = self.request.GET.get("q", "").strip()
        genre = self.request.GET.get("genero", "").strip()
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(synopsis__icontains=search))
        if genre:
            queryset = queryset.filter(genres__id=genre)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["selected_genre"] = self.request.GET.get("genero", "")
        context["search_query"] = self.request.GET.get("q", "")
        recent_ids = self.request.session.get("recent_anime_ids", [])
        if isinstance(recent_ids, list):
            recent_ids = [
                anime_id
                for anime_id in recent_ids
                if isinstance(anime_id, int) and not isinstance(anime_id, bool)
            ]
            recent = Anime.objects.filter(pk__in=recent_ids).prefetch_related("genres")
            recent_by_id = {anime.pk: anime for anime in recent}
            context["recent_animes"] = [
                recent_by_id[anime_id] for anime_id in recent_ids if anime_id in recent_by_id
            ]
        else:
            context["recent_animes"] = []
        return context


class AnimeDetailView(DetailView):
    model = Anime
    template_name = "catalog/anime_detail.html"
    context_object_name = "anime"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        episodes = Episode.objects.order_by("number")
        return Anime.objects.prefetch_related(
            "genres", Prefetch("seasons__episodes", queryset=episodes)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_ids = self.request.session.get("recent_anime_ids", [])
        if not isinstance(recent_ids, list):
            recent_ids = []
        recent_ids = [
            anime_id
            for anime_id in recent_ids
            if isinstance(anime_id, int) and not isinstance(anime_id, bool)
        ]
        recent_ids = [self.object.pk] + [
            anime_id for anime_id in recent_ids if anime_id != self.object.pk
        ]
        self.request.session["recent_anime_ids"] = recent_ids[:12]
        context["is_favorite"] = (
            self.request.user.is_authenticated
            and Favorite.objects.filter(user=self.request.user, anime=self.object).exists()
        )
        return context


class AnimeCreateView(CreateView):
    model = Anime
    form_class = AnimeForm
    template_name = "catalog/anime_form.html"

    @method_decorator(staff_member_required(login_url="login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Anime cadastrado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class AnimeUpdateView(UpdateView):
    model = Anime
    form_class = AnimeForm
    template_name = "catalog/anime_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    @method_decorator(staff_member_required(login_url="login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Anime atualizado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


@login_required
def toggle_favorite(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, anime=anime)
    if not created:
        favorite.delete()
        messages.info(request, "Anime removido dos favoritos.")
    else:
        messages.success(request, "Anime adicionado aos favoritos.")
    return redirect("catalog:anime_detail", slug=anime.slug)


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("anime").prefetch_related(
        "anime__genres"
    )
    return render(request, "catalog/favorites.html", {"favorites": favorites})
