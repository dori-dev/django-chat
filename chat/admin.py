"""chat admin
"""
from csv import list_dialects
from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import Message, Chat, Customize


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


class CustomizeAdmin(admin.ModelAdmin):
    list_display = ("name", "describe", "show_color")

    def show_color(self, model: Customize):
        color = model.color
        html = f'<p style="color: {color}">{color}</p>'
        return format_html(html)

    show_color.short_description = "رنگ"


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Customize, CustomizeAdmin)
