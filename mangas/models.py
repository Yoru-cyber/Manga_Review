from django.db import models
from django.contrib.auth.models import User

class Manga(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="mangas_images/", null=True, blank=True)
    genres = models.ManyToManyField("Genre")
    publication_year = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("Activo", "Activo"),
            ("Completado", "Completado"),
            ("Hiatus", "Hiatus"),
        ],
    )

    def __str__(self):
        return f'{self.title} {self.author} {self.publication_year}, {self.genres}'


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    date = models.DateField()
    review = models.TextField()

    def __str__(self):
        return f'{self.user} {self.manga} {self.date}'


# Create your models here.
