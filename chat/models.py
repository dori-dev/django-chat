"""models of chat app
"""
from typing import List
from django.db.models.query import QuerySet
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

    @staticmethod
    def best_group() -> list:
        all_room: QuerySet[Chat] = Chat.objects.all().order_by('timestamp')
        rooms: List[tuple] = list(
            map(lambda room: (room.name, room.members.count()), all_room))
        sorted_rooms = sorted(
            rooms, key=lambda room: room[1], reverse=True)
        best_room = list(
            map(lambda room: room[0], sorted_rooms[:8]))
        return best_room

    @staticmethod
    def last_group() -> list:
        all_room: QuerySet[Chat] = Chat.objects.all().order_by(
            "-timestamp")[:8]
        last_room = list(
            map(lambda room: room.name, all_room))
        return last_room

    @staticmethod
    def your_group(user) -> list:
        chats: QuerySet[Chat] = Chat.objects.filter(
            members__username=user).order_by('-members')
        chat_names = list(
            map(lambda chat: chat.name, chats))
        return chat_names

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


# 'add', 'aggregate', 'alias', 'all', 'annotate', 'auto_created', 'bulk_create', 'bulk_update', 'check', 'clear', 'complex_filter', 'contains', 'contribute_to_class', 'core_filters', 'count', 'create', 'create_superuser', 'create_user', 'creation_counter', 'dates', 'datetimes', 'db', 'db_manager', 'deconstruct', 'defer', 'difference', 'distinct', 'do_not_call_in_templates', 'earliest', 'exclude', 'exists', 'explain', 'extra', 'filter', 'first', 'from_queryset', 'get', 'get_by_natural_key', 'get_or_create', 'get_prefetch_queryset', 'get_queryset', 'in_bulk', 'instance', 'intersection', 'iterator', 'last', 'latest', 'make_random_password', 'model', 'name', 'none', 'normalize_email', 'only', 'order_by', 'pk_field_names', 'prefetch_cache_name', 'prefetch_related', 'query_field_name', 'raw', 'related_val', 'remove', 'reverse', 'select_for_update', 'select_related', 'set', 'source_field', 'source_field_name', 'symmetrical', 'target_field', 'target_field_name', 'through', 'union', 'update', 'update_or_create', 'use_in_migrations', 'using', 'values', 'values_list', 'with_perm'
