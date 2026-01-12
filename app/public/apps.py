from django.apps import AppConfig
import os


class PublicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.public"

    def ready(self):
        # Only run in the main process, not in the autoreloader process
        if os.environ.get("RUN_MAIN") == "true":
            from app.public.loop import start

            start()
