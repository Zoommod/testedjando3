from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from decouple import config

class UserAdmin(admin.ModelAdmin):
    # campos de visualização geral dos dados
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_groups']

    # filtros da visualização geral
    list_filter = ['groups']

    # campos somente leitura
    readonly_fields = ['date_joined']

    # campos de busca
    search_fields = ['email', 'username', 'first_name', 'last_name']

    # texto abaixo do input de busca
    search_help_text = 'Pesquisa realizada por nome, email e usuário (matrícula)'

    # estrutura dos formulários
    fieldsets = [
        (
            'Informações pessoais',
            {
                "fields": ['username', 'email', ('first_name', 'last_name')],
            },
        ),
        (
            'Informações do sistema',
            {
                "fields": ['groups', 'date_joined'],
            },
        ),
    ]

    # método para personalização do campo de groups na visualização geral dos dados
    def get_groups(self, obj):
        cargos = ', '.join([group.name for group in obj.groups.all()])
        return cargos if cargos else 'Não tem cargos'
    get_groups.short_description = 'Cargos'

    # sobrescrita do fieldset para remover o 'date_joined' do addform
    def get_fieldsets(self, request, obj):
        # Obtém os fieldsets padrão
        fieldsets = super().get_fieldsets(request, obj)

        # Remova o campo que você deseja excluir do formulário de adição
        if obj is None:
            for fieldset in fieldsets:
                if 'fields' in fieldset[1] and 'date_joined' in fieldset[1]['fields']:
                    fieldset[1]['fields'].remove('date_joined')

        return fieldsets

    # sobrescrita do get_form para mudar o label dos formulários e
    #   para remover o 'date_joined' do addform
    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Altere o label do campo
        form.base_fields['groups'].label = 'Cargos'

        # Remove o campo apenas ao adicionar um novo objeto
        if obj is None:
            if 'date_joined' in form.base_fields:
                del form.base_fields['date_joined']

        return form
    
    # sobrescrita do readonly_fields para remover o 'date_joined' do 
    #   addform
    def get_readonly_fields(self, request, obj):
        # Lista de campos que serão somente leitura
        readonly_fields = super().get_readonly_fields(request, obj)
        
        # Remova o campo que você deseja excluir do formulário de adição
        if obj is None:
            readonly_fields = list(readonly_fields)
            readonly_fields.remove('date_joined')

        return readonly_fields

    # sobrescrita do save_model para enviar um email para o usuário 
    #   com login e senha
    def save_model(self, request, obj, form, change):
        # Gere uma senha de primeiro acesso e a atribua ao usuário
        temp_password = User.objects.make_random_password()
        obj.password = make_password(temp_password, salt=None, hasher='default')

        # Salve o usuário
        super().save_model(request, obj, form, change)

        # email padrão com texto
        msg = EmailMultiAlternatives(
            "O sistema da PROEX te recebe de braços abertos!", 
            f"O seu usuário é: {obj.username} e sua senha de primeiro acesso é: {temp_password}",
            config('EMAIL_HOST_USER'),
            [obj.email],
        )

        # email em html
        msg.attach_alternative(
            f"<h1>Olá!</h1><p>Essas são suas crendenciais para no novo sistema da PROEX:</p><br/><strong>Usuário: </strong> <p>{obj.username}</p><br/><strong>Senha: </strong> <p>{temp_password}</p><br/> <p>Acesse o sistema em: <a href='http://localhost:8000/admin'>http://proex.com</a></p>", 
            "text/html"
        )

        # enviar email
        msg.send(fail_silently=False)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)