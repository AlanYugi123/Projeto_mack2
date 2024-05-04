from django.urls import path, include
from app_mack import views

urlpatterns = [

    path('',views.Pagina_login,name='Pagina_login'),

    path('login/', views.login_view, name='login'),

    path('ola_mundo/',views.ola_mundo_view,name='pagina_ola_mundo'),

    path('escolher_momento/', views.escolher_momento, name='escolher_momento'),

    path('iniciar_registro/', views.iniciar_registro, name='iniciar_registro'),

    path('salvar_presencas/', views.salvar_presencas, name='salvar_presencas'),

    path('gerar_relatorio/', views.gerar_relatorio, name='gerar_relatorio'),

    path('confirmacao_presenca/', views.confirmacao_presenca, name='confirmacao_presenca'),

    path('download_xlsx/', views.download_xlsx, name='download_xlsx')

]