from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:manga_id>/", views.details, name="details"),
    path("login/", views.loginUser, name="login"),
    path("user/logout/", views.logoutUser, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("<int:manga_id>/user/review/", views.createReview, name="createReview"),
]
