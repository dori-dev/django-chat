from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def last_messages():
        return Message.objects.order_by("-timestamp").all()

    def author_username(self):
        return self.author.username

    def __str__(self):
        return "message"  # TODO use chat_room and author, ....
