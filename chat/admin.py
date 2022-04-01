"""chat admin
"""
from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "message", "time", "room")
    list_filter = ("author", "room", "timestamp")
    search_fields = ("content",)

    def time(self, model: Message):
        date: datetime = model.timestamp.astimezone()
        format_date = datetime.strftime(date, "%b %d, %H:%M:%S")
        return format_date

    def message(self, model: Message):
        content = model.content
        if model.type == "image":
            return format_html(f'<a href="{content}">تصویر</a>')
        return content

    time.short_description = "زمان"
    message.short_description = "پیام"


class ChatAdmin(admin.ModelAdmin):
    list_display = ("name", "members_count", "messages", "time")
    list_filter = ("members", "timestamp")
    search_fields = ("name",)

    def members_count(self, model: Chat):
        return model.members.count()

    def messages(self, model: Chat):
        messages = Message.objects.filter(room=model)
        return len(messages)

    def time(self, model: Chat):
        date: datetime = model.timestamp.astimezone()
        format_date = datetime.strftime(date, "%b %d, %H:%M:%S")
        return format_date
    time.short_description = "زمان ایجاد"
    members_count.short_description = "تعداد اعضا"
    messages.short_description = "تعداد پیام ها"


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
