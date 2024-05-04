from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Adicione o related_name aqui
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Adicione o related_name aqui
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    turma = models.CharField(max_length=50)
    ano = models.CharField(max_length=10)

    def __str__(self):
        return self.nome


class RegistroPresenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)  # Ligação com o modelo Aluno
    matricula = models.CharField(max_length=20)
    turma = models.CharField(max_length=50)
    ano = models.CharField(max_length=10)
    data = models.DateField(default=date.today)  # Armazena a data do registro
    materia = models.CharField(max_length=100)
    status = models.CharField(max_length=50)  # 'Presente' ou 'Faltou'

    def __str__(self):
        return f"{self.aluno.nome} ({self.data.strftime('%d/%m/%Y')}) - {self.status}"