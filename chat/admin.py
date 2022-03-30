"""chat admin
"""
from datetime import datetime
from django.contrib import admin
from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "time", "room")
    list_filter = ("author", "room", "timestamp")

    def time(self, model: object):
        date: datetime = model.timestamp.astimezone()
        format_date = datetime.strftime(date, "%b %d, %H:%M:%S")
        return format_date
    time.short_description = "زمان"


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
