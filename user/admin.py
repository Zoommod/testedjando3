from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from decouple import config

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_groups']
    list_filter = ['groups']
    readonly_fields = ['date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    search_help_text = 'Pesquisa realizada por nome, email e usuário (matrícula)'

    fieldsets = [
        (
            'Informações pessoais',
            {
                "fields": ['username', 'email', ('first_name', 'last_name')],
            },
        ),
        (
            'Cargos do sistema',
            {
                "fields": ['groups'],
            },
        ),
        (
            "Informações extra",
            {
                "classes": ["collapse"],
                "fields": ['date_joined'],
            },
        ),
    ]

    def get_groups(self, obj):
        cargos = ', '.join([group.name for group in obj.groups.all()])
        return cargos if cargos else 'Não tem cargos'
    get_groups.short_description = 'Cargos'

    def save_model(self, request, obj, form, change):
        # Gere uma senha de primeiro acesso e a atribua ao usuário
        temp_password = User.objects.make_random_password()
        obj.set_password(temp_password)

        # Salve o usuário
        super().save_model(request, obj, form, change)

        # Envie um e-mail ao usuário com a senha gerada
        send_mail(
            "O sistema da PROEX te recebe de braços abertos!",
            f"O seu usuário é: {obj.username} e sua senha de primeiro acesso é: {temp_password}",
            config('EMAIL_HOST_USER'),
            [obj.email],
            fail_silently=False,
        )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)