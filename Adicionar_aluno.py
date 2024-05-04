from app_mack.models import Aluno
import random

# Definição das turmas e anos
turmas = ['Turma A', 'Turma B']
anos = ['1º Ano', '2º Ano', '3º Ano', '4º Ano', '5º Ano']

# Criando alunos para cada combinação de turma e ano
for turma in turmas:
    for ano in anos:
        for i in range(1, 31):  # Criar 30 alunos para cada combinação
            nome = f'Aluno {i} {turma} {ano}'
            matricula = f'{turma[6]}{ano[0]}{str(i).zfill(3)}'  # Gera uma matrícula única
            aluno = Aluno(nome=nome, matricula=matricula, turma=turma, ano=ano)
            aluno.save()
            print(f'Criado: {nome} - Matrícula: {matricula} - Turma: {turma} - Ano: {ano}')