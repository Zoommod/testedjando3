from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def create_permissions():
    coordenadores, created = Group.objects.get_or_create(name='Coordenadores')
    criadores_de_conteudo, created = Group.objects.get_or_create(name='Criadores de Conteúdo')
    moderadores, created = Group.objects.get_or_create(name='Moderadores')
    administradores, created = Group.objects.get_or_create(name='Administradores')

    # aqui é criado uma nova permissão para publicar notícias
    content_type = ContentType.objects.get_for_model(User)
    permission_publish, created = Permission.objects.get_or_create(
        codename='can_publish',
        name='Can Publish News',
        content_type=content_type,
    )
    if created:
        # é adicionada a permissão de publicar ao grupo de administradores
        administradores.permissions.add(permission_publish)

    # nova permissão para criar notícias
    permission_create, created = Permission.objects.get_or_create(
        codename='can_create',
        name='Can Create News',
        content_type=content_type,
    )
    if created:
        # permissão de criar ao grupo de criadores de conteúdo
        criadores_de_conteudo.permissions.add(permission_create)

    # nova permissão para moderar notícias
    permission_moderate, created = Permission.objects.get_or_create(
        codename='can_moderate',
        name='Can Moderate News',
        content_type=content_type,
    )
    if created:
        # permissão de moderar ao grupo de moderadores
        moderadores.permissions.add(permission_moderate)

    # nova permissão para coordenar notícias
    permission_coordinate, created = Permission.objects.get_or_create(
        codename='can_coordinate',
        name='Can Coordinate News',
        content_type=content_type,
    )
    if created:
        # permissão de coordenar ao grupo de coordenadores
        coordenadores.permissions.add(permission_coordinate)

create_permissions()
