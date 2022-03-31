"""chat admin
"""
from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "message", "time", "room")
    list_filter = ("author", "room", "timestamp")

    def time(self, model: object):
        date: datetime = model.timestamp.astimezone()
        format_date = datetime.strftime(date, "%b %d, %H:%M:%S")
        return format_date

    def message(self, model: object):
        content = model.content
        if model.type == "image":
            return format_html(f'<a href="{content}">تصویر</a>')
        return content

    time.short_description = "زمان"
    message.short_description = "پیام"


class ChatAdmin(admin.ModelAdmin):
    list_display = ("name", "members_count", "time")
    list_filter = ("members", "timestamp")

    def members_count(self, model: object):
        return model.members.count()

    def time(self, model: object):
        date: datetime = model.timestamp.astimezone()
        format_date = datetime.strftime(date, "%b %d, %H:%M:%S")
        return format_date
    time.short_description = "زمان ایجاد"
    members_count.short_description = "تعداد اعضا"


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
