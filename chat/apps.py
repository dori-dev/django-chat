from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    verbose_name = "گفتگو"

    def ready(self):
        try:
            from .models import Customize
            if len(Customize.objects.all()) == 0:
                Customize.create_default_fields()
        except Exception:
            pass
