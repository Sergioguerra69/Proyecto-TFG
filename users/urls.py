# URLs: enlazamos las rutas del navegador con las funciones de views.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs de autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    
    # URLs para admin
    path('agentes/', views.lista_agentes, name='lista_agentes'),
    
    # URLs para solicitudes de servicios
    path('solicitar/consulta/', views.solicitar_consulta, name='solicitar_consulta'),
    path('solicitar/analisis/', views.solicitar_analisis, name='solicitar_analisis'),
    path('solicitar/cirugia/', views.solicitar_cirugia, name='solicitar_cirugia'),
    path('solicitar/urgencia/', views.solicitar_urgencia, name='solicitar_urgencia'),
    
    # URL para ver las citas del usuario
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    
    # URLs de administración (solo para admin/veterinarios)
    path('admin/panel/', views.panel_admin, name='panel_admin'),
    path('admin/usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('admin/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('admin/usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('admin/citas/', views.gestionar_citas, name='gestionar_citas'),
    path('admin/reportes/', views.reportes, name='reportes'),
]