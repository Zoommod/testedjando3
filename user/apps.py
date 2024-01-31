# user/apps.py

from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver
        from user.permissions import create_permissions

        # aqui vai conectar a função create_permissions ao sinal post_migrate
        @receiver(post_migrate)
        def post_migrate_handler(sender, **kwargs):
            create_permissions()

        # vai garantir que a função seja conectada apenas uma vez
        post_migrate.connect(post_migrate_handler, sender=self)
