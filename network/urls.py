
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:target>", views.profile, name="profile"),
    path("edit_post/<str:post_id>", views.edit_post, name="edit_post"),
    path("following", views.following, name="following"),
    path("follow/<str:target_id>", views.follow, name="follow"),
]
