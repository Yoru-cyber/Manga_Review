from django.shortcuts import redirect, render
from django.template import loader
from django.http import Http404, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Anime, Manga, Review


def index(request):
    try:
        mangas = Manga.objects.all().order_by("-id")[:10]
    except Exception:
        raise Http404("Something went wrong")
    context = {"mangas": mangas}
    return render(
        template_name="mangas/mangas/index.html", request=request, context=context
    )


# Create your views here.
def details(request, manga_id: int):
    try:
        manga = Manga.objects.get(pk=manga_id)
    except Manga.DoesNotExist:
        raise Http404("Question does not exist")
    try:
        reviews = manga.review_set.all()
    except Review.DoesNotExist:
        reviews = []
    manga_genres_str = ", ".join(manga.genres.all().values_list("name", flat=True))
    context = {"manga": manga, "reviews": reviews, "genres": manga_genres_str}
    return render(
        template_name="mangas/mangas/details.html", request=request, context=context
    )


def loginUser(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists() is False:
            messages.error(request, "El usuario no existe")
            return redirect("index")
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("index")
        else:
            messages.error(request, "Usuario o contraseña incorrecta")
    return render(template_name="mangas/login_user.html", request=request, context={})


def logoutUser(request):
    logout(request=request)
    return redirect("index")


def signup(request: HttpRequest):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("index")
    context = {"form": form}
    return render(template_name="mangas/signup.html", request=request, context=context)


@login_required()
def createReview(request: HttpRequest, manga_id: int):
    review = None
    user_id = request.user.id
    try:
        manga = Manga.objects.get(pk=manga_id)
    except Manga.DoesNotExist:
        manga = None
    try:
        review = manga.review_set.get(user=user_id)
    except Review.DoesNotExist:
        review = None
    if request.method == "POST":
        date = timezone.now()
        user_review = request.POST.get("review")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            user = None
        Review.objects.update_or_create(
            user=user, manga=manga, defaults={"date": date, "review": user_review}
        )
        return redirect(request.META["HTTP_REFERER"])
    context = {"review": review}
    return render(
        template_name="mangas/mangas/create_review.html",
        request=request,
        context=context,
    )


def animeIndex(request):
    try:
        animes = Anime.objects.all().order_by("-id")[:10]
    except Exception:
        raise Http404("Something went wrong")
    context = {"animes": animes}
    return render(
        template_name="mangas/anime/index.html", request=request, context=context
    )


def animeDetails(request, anime_id: int):
    try:
        anime = Anime.objects.get(pk=anime_id)
    except Anime.DoesNotExist:
        raise Http404("Question does not exist")
    # try:
    #     reviews = anime.review_set.all()
    # except Review.DoesNotExist:
    #     reviews = []

    anime_genres_str = ", ".join(anime.genres.all().values_list("name", flat=True))
    context = {"anime": anime, "reviews": [], "genres": anime_genres_str}
    return render(
        template_name="mangas/anime/details.html", request=request, context=context
    )
