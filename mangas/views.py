from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Manga


def index(request):
    try:
        mangas = Manga.objects.all()
    except Manga.DoesNotExist:
        raise Http404("Question does not exist")
    context = {"mangas": mangas}
    return render(template_name="mangas/index.html", request=request, context=context)


# Create your views here.
def details(request, manga_id):
    try:
        manga = Manga.objects.get(pk=manga_id)
    except Manga.DoesNotExist:
        raise Http404("Question does not exist")
    context = {"manga": manga}
    return render(template_name="mangas/details.html", request=request, context=context)
