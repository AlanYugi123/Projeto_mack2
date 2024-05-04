import os
import django
from django.conf import settings

# Defina a variável de ambiente DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto_mack.settings')

# Carregue as configurações do Django
django.setup()

# Agora você pode importar seus modelos e interagir com o banco de dados
from django.contrib.auth.models import User

user = User.objects.create_user('alan', 'alan@example.com', 'senha123')

user.save()