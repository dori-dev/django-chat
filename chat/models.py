from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(
        default='welcome', max_length=256,
        null=False, blank=False)

    @staticmethod
    def last_messages(room_name: str):
        return Message.objects.filter(
            room_name=room_name).order_by("timestamp").all()

    def author_username(self):
        return self.author.username

    def __str__(self):
        return "message"  # TODO use chat_room and author, ....
