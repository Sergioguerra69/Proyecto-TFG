from django.contrib import admin
from .models import Servicio

# Registramos el modelo para que aparezca en el panel /admin
admin.site.register(Servicio)
