from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    room_name = models.CharField(
        max_length=256,
        null=False, blank=False)
    members = models.ManyToManyField(  # TODO for `popular room` and `your room`
        User,
        blank=False)
    # timestamp = models.DateTimeField(  # TODO for `last room`
    #     auto_now_add=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True)
    room_name = models.CharField(
        default='welcome', max_length=256,
        null=False, blank=False,
        verbose_name="room")
    # room_name = models.ForeignKey(
    #     Chat, on_delete=models.CASCADE,
    #     null=False, blank=False)

    @staticmethod
    def last_messages(room_name: str):
        return Message.objects.filter(
            room_name=room_name).order_by("-timestamp")[:32]

    def author_username(self):
        return self.author.username

    def __str__(self):
        return f'"{self.author}" message in the "{self.room_name}" room'
