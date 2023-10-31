from django.apps import AppConfig


class ServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service"

    def get_model(self, model_name, require_ready=True):
        from .signals import create_profile, save_profile
