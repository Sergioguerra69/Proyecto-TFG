from django.contrib import admin
from .models import Producto

# Registramos el modelo para que el profe vea que sabemos usar el Admin de Django
admin.site.register(Producto)
