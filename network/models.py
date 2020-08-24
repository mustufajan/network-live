from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("network.User", related_name='followers', blank=True)

class Post(models.Model):
    text = models.CharField(max_length=500)
    timestamp=models.DateTimeField(auto_now_add=True)
    poster=models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    likes=models.IntegerField(default=0)
    likers = models.ManyToManyField('User', related_name="liked_posts", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster_id": self.poster.id,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
        }

    def __str__(self):
        return f"{self.text} by {self.poster} on {self.timestamp}"

