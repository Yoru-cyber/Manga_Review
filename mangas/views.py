from django.shortcuts import redirect, render
from django.template import loader
from django.http import Http404, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Manga


def index(request):
    try:
        mangas = Manga.objects.all()
    except Manga.DoesNotExist:
        raise Http404("Question does not exist")
    context = {"mangas": mangas}
    return render(template_name="mangas/index.html", request=request, context=context)


# Create your views here.
def details(request, manga_id: int):
    try:
        manga = Manga.objects.get(pk=manga_id)
    except Manga.DoesNotExist:
        raise Http404("Question does not exist")
    context = {"manga": manga}
    return render(template_name="mangas/details.html", request=request, context=context)


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
