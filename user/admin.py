from django.contrib import admin
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',  'first_name', 'last_name']
    fields = ('username', 'email', ('first_name', 'last_name'), 'date_joined')
    # question: tem como fazer a listagem por group?
    list_filter = []
    readonly_fields = ['date_joined']
    search_fields= ['email','username',  'first_name', 'last_name']
    search_help_text = 'Pesquisa realizada por nome, email e usuário (matrícula)'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
