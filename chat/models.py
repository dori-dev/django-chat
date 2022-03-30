"""models of chat app
"""
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    name = models.CharField(
        default='welcome', max_length=256,
        null=False, blank=False,
        verbose_name="گروه")
    members = models.ManyToManyField(
        User,
        blank=False)
    timestamp = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="کاربر")
    content = models.TextField(verbose_name="پیام")
    timestamp = models.DateTimeField(
        auto_now_add=True)
    room = models.ForeignKey(
        Chat, on_delete=models.CASCADE,
        null=False, blank=False,
        verbose_name="گروه")

    @staticmethod
    def last_messages(room_name: str):
        room = Chat.objects.get(name=room_name)
        return Message.objects.filter(
            room=room).order_by("-timestamp")[:22]

    def author_username(self):
        return self.author.username

    def __str__(self):
        return f'پیام "{self.author}" در گروه "{self.room}"'
