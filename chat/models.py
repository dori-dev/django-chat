"""models of chat app
"""
from datetime import datetime
from typing import List
from django.db.models.query import QuerySet
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


def unique_string():
    random_string: str = get_random_string(8)
    all_room_id: QuerySet[Chat] = Chat.objects.all()
    rooms_id = list(
        map(lambda chat: chat.room_id, all_room_id))
    while random_string in rooms_id:
        random_string: str = get_random_string(8)
        print(random_string)
    return random_string


def remove_listener(list_: list) -> list:
    if "listener" in list_:
        list_.remove("listener")
    return list_


class Chat(models.Model):
    name = models.CharField(
        default='welcome', max_length=256,
        null=False, blank=False,
        verbose_name="گروه")
    members = models.ManyToManyField(
        User,
        blank=False,
        verbose_name="اعضا")
    timestamp = models.DateTimeField(
        auto_now_add=True)
    room_id = models.CharField(
        default=unique_string,
        unique=True,
        editable=False,
        max_length=8)

    @staticmethod
    def best_group() -> list:
        all_room: QuerySet[Chat] = Chat.objects.all().order_by('timestamp')
        rooms: List[tuple] = list(
            map(lambda room: (room.name,
                              len(Message.objects.filter(room=room)),
                              room.members.count()), all_room)
        )
        busy_rooms = sorted(
            rooms, key=lambda room: room[1], reverse=True)
        sorted_rooms = sorted(
            busy_rooms, key=lambda room: room[2], reverse=True)
        best_room = list(
            map(lambda room: room[0], sorted_rooms[:7]))
        return remove_listener(best_room)

    @staticmethod
    def last_group() -> list:
        all_room: QuerySet[Chat] = Chat.objects.all().order_by(
            "-timestamp")[:7]
        last_room = list(
            map(lambda room: room.name, all_room))
        return remove_listener(last_room)

    @staticmethod
    def your_group(user) -> list:
        chats: QuerySet[Chat] = Chat.objects.filter(
            members__username=user)
        group_messages: List[tuple] = []
        for chat in chats:
            chat_name = chat.name
            try:
                last_message: Message = Message.objects.filter(
                    room=chat).order_by("-timestamp")[0]
            except IndexError:
                continue
            message_time: datetime = last_message.timestamp
            group_messages.append((chat_name, message_time))
        sorted_chats = sorted(group_messages, reverse=True,
                              key=lambda data: data[1])
        chat_names = list(
            map(lambda chat: chat[0], sorted_chats))
        return remove_listener(chat_names)

    @staticmethod
    def all_groups() -> list:
        all_group = Chat.objects.all()
        groups = list(
            map(lambda group: group.name, all_group)
        )
        return remove_listener(groups)

    @staticmethod
    def get_members_list(room_id: str):
        room: Chat = Chat.objects.get(room_id=room_id)
        members = list(
            map(lambda user: user.username, room.members.all())
        )
        return members

    class Meta:
        verbose_name_plural = "گروه ها"
        verbose_name = "گروه"

    def __str__(self):
        return self.name


class Message(models.Model):
    TYPES = (
        ('message', 'پیام'),
        ('image', 'عکس'),
    )
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
    type = models.CharField(
        max_length=32,
        choices=TYPES,
        default="message",
        verbose_name="نوع")

    @staticmethod
    def last_messages(room_id: str):
        room = Chat.objects.get(room_id=room_id)
        return Message.objects.filter(
            room=room).order_by("-timestamp")[:22]

    def author_username(self):
        return self.author.username

    def __str__(self):
        return f'پیام "{self.author}" در گروه "{self.room}"'

    class Meta:
        verbose_name_plural = "پیام ها"
        verbose_name = "پیام"
