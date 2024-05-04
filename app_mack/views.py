from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Aluno
from .models import RegistroPresenca
import datetime
from django.contrib import messages
from django.http import HttpResponse
import openpyxl

from django.http import HttpResponseRedirect

def Pagina_login(request):

    return render(request, 'app_mack/Pagina_login.html')


def login_view(request):
    # Mensagem de erro inicialmente vazia
    error_message = 'Login/Senha inválido'

    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['password']
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('pagina_ola_mundo')
        else:
            # Definindo a mensagem de erro se a autenticação falhar
            error_message = 'Nome de usuário ou senha inválido.'

    # Passar a mensagem de erro para o template
    return render(request, 'app_mack/Pagina_login.html', {'error_message': error_message})

def ola_mundo_view(request):
    if request.method == 'POST':
        request.session['turma'] = request.POST.get('turma', '')
        request.session['ano'] = request.POST.get('ano', '')
        request.session['materia'] = request.POST.get('materia', '')
        show_options = True  # Exibir as opções após o envio do formulário
    else:
        show_options = False

    context = {
        'turma': request.session.get('turma', ''),
        'ano': request.session.get('ano', ''),
        'materia': request.session.get('materia', ''),
        'show_options': show_options
    }

    print(context)

    return render(request, 'app_mack/ola_mundo.html', context)



def escolher_momento(request):

    return render(request, 'app_mack/escolher_momento.html')



def iniciar_registro(request):
    turma = request.session.get('turma', 'Turma padrão')
    ano = request.session.get('ano', 'Ano padrão')
    materia = request.session.get('materia', 'Matéria padrão')
    data = request.session.get('data', datetime.date.today().strftime('%Y-%m-%d'))

    # Buscar alunos baseados na turma e no ano
    alunos = Aluno.objects.filter(turma=turma, ano=ano)

    context = {
        'turma': turma,
        'ano': ano,
        'materia': materia,
        'data': data,
        'alunos': alunos  # Passando alunos para o template
    }

    return render(request, 'app_mack/registro_presencas.html', context)

def salvar_presencas(request):
    if request.method == 'POST':
        turma = request.session.get('turma', 'Turma padrão')
        ano = request.session.get('ano', 'Ano padrão')
        materia = request.session.get('materia', 'Matéria padrão')
        data = datetime.date.today()

        for key, value in request.POST.items():
            if key.startswith('presenca_'):
                aluno_id = key.split('_')[1]
                aluno = Aluno.objects.get(id=aluno_id)

                # Antes de salvar um novo registro, remover registros anteriores para o mesmo aluno, turma, ano, matéria e data
                RegistroPresenca.objects.filter(
                    aluno=aluno,
                    turma=turma,
                    ano=ano,
                    materia=materia,
                    data=data
                ).delete()

                # Salvar o novo registro
                RegistroPresenca.objects.create(
                    aluno=aluno,
                    matricula=aluno.matricula,
                    turma=turma,
                    ano=ano,
                    data=data,
                    materia=materia,
                    status=value
                )

        return HttpResponseRedirect('/confirmacao_presenca/')
    else:
        return HttpResponseRedirect('/iniciar_registro/')  # Redireciona se não for POST ou ocorrer erro

def confirmacao_presenca(request):

    return render(request, 'app_mack/confirmacao_presenca.html')


def gerar_relatorio(request):
    if request.method == 'POST':
        data_escolhida = request.POST.get('data_escolhida')
        turma = request.session.get('turma')
        ano = request.session.get('ano')
        materia = request.session.get('materia')

        # Filtrar registros baseados em turma, ano, matéria e data
        registros = RegistroPresenca.objects.filter(turma=turma, ano=ano, materia=materia, data=data_escolhida)

        # Armazenar critérios de filtragem na sessão
        request.session['filtro'] = {
            'turma': turma,
            'ano': ano,
            'materia': materia,
            'data': data_escolhida
        }

        return render(request, 'app_mack/relatorio_presencas.html', {'registros': registros, 'data': data_escolhida})
    else:
        return redirect('/ola_mundo/')  # Ou uma URL de erro


def download_xlsx(request):
    # Recuperar critérios de filtragem da sessão
    filtro = request.session.get('filtro', {})
    registros = RegistroPresenca.objects.filter(
        turma=filtro.get('turma', ''),
        ano=filtro.get('ano', ''),
        materia=filtro.get('materia', ''),
        data=filtro.get('data', '')
    )

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="filtered_report.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Nome do Aluno', 'Matrícula', 'Turma', 'Ano', 'Data', 'Matéria', 'Status'])

    for registro in registros:
        ws.append([
            registro.aluno.nome,
            registro.matricula,
            registro.turma,
            registro.ano,
            registro.data.strftime('%Y-%m-%d'),
            registro.materia,
            registro.status
        ])

    wb.save(response)
    return response