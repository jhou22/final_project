from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    # Implicitly connect signal handlers decorated with @receiver.
    def ready(self):
        from . import signals
        return super().ready()
