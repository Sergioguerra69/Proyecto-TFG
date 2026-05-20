# URLs de usuarios - login, registro y perfiles
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login y registro
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),

    # Recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    # Panel de administrador
    path('agentes/', views.lista_agentes, name='lista_agentes'),

    # Solicitudes de servicios
    path('solicitar/consulta/', views.solicitar_consulta, name='solicitar_consulta'),
    path('solicitar/analisis/', views.solicitar_analisis, name='solicitar_analisis'),
    path('solicitar/cirugia/', views.solicitar_cirugia, name='solicitar_cirugia'),
    path('solicitar/urgencia/', views.solicitar_urgencia, name='solicitar_urgencia'),

    # Citas del usuario
    path('mis-citas/', views.mis_citas, name='mis_citas'),

    # Administración del sistema
    path('admin/panel/', views.panel_admin, name='panel_admin'),
    path('admin/usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('admin/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('admin/usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('admin/citas/', views.gestionar_citas, name='gestionar_citas'),
    path('admin/reportes/', views.reportes, name='reportes'),
]