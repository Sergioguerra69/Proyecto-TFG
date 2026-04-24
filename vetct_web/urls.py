# URLs: enlazamos las rutas del navegador con las funciones de views.py
"""
URL configuration for vetct_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
CONFIGURACIÓN DE URLS PARA EL TFG VETCT
Aquí definimos todas las rutas de nuestro sitio web.
Cada ruta lleva a una página diferente.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos las vistas (Lo que hace que cada página funcione)
from inicio import views as inicio_views
from servicios import views as servicios_views
from tienda import views as tienda_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Página de inicio
    path('', inicio_views.home, name='home'),
    path('inicio/', inicio_views.home, name='home_slash'),
    path('nosotros/', inicio_views.nosotros, name='nosotros'),
    path('equipo/', inicio_views.equipo, name='equipo'),
    
    # API de métricas para el JavaScript
    path('api/clic-metrica/', inicio_views.clic_metrica, name='clic_metrica'),
    
    # Servicios y Tienda
    path('servicios/', servicios_views.lista_servicios, name='servicios'),
    path('tienda/', tienda_views.lista_productos, name='tienda'),
    path('tienda/nuevo_producto/', tienda_views.nuevo_producto, name='nuevo_producto'),
    # Usuarios, Contacto y Notificaciones
    path('users/', include('users.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('contacto/', include('contacto.urls')),
    
    # Módulos Especializados (Modularidad del TFG)
    path('consultas/', include('consultas.urls')),
    path('laboratorio/', include('laboratorio.urls')),
    path('urgencias/', include('urgencias.urls')),
    path('estetica/', include('estetica.urls')),
    path('cirugias/', include('cirugias.urls')),

    # API REST MANUAL (Requisito de 2º DAW)
    path('api/servicios/', servicios_views.api_servicios, name='api_servicios'),
    path('api/productos/', tienda_views.api_productos, name='api_productos'),
]

# Configuración para ver las fotos (media) durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)