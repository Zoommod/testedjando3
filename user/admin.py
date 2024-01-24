from django.contrib import admin
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_groups']
    fields = ('username', 'email', ('first_name', 'last_name'), 'groups', 'date_joined')
    list_filter = ['groups']
    readonly_fields = ['date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    search_help_text = 'Pesquisa realizada por nome, email e usuário (matrícula)'

    def get_groups(self, obj):
        cargos = ', '.join([group.name for group in obj.groups.all()])
        return cargos if cargos else 'Não tem cargos'
    get_groups.short_description = 'Cargos'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)