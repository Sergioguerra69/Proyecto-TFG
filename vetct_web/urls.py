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
from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static  
from django.urls import path, include

from inicio import views as inicio_views
from django.shortcuts import render  

# Views simples para las otras apps
def servicios_view(request):
    return render(request, 'servicios/index.html')

def contacto_view(request):
    return render(request, 'contacto/index.html')

def tienda_view(request):
    return render(request, 'tienda/index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio_views.home, name='home'),
    path('nosotros/', inicio_views.nosotros, name='nosotros'),
    path('equipo/', inicio_views.equipo, name='equipo'),
    path('servicios/', servicios_view, name='servicios'),
    path('contacto/', contacto_view, name='contacto'),
    path('tienda/', tienda_view, name='tienda'),
     path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)