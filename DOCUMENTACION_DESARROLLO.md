# Documentación del Proyecto - Sistema de Gestión Veterinaria VetCT

## Descripción del Proyecto

VetCT es una aplicación web para gestionar clínicas veterinarias. Está desarrollada con Django (para la parte del servidor) y Tailwind CSS (para el diseño). El sistema permite gestionar pacientes, organizar citas y coordinar el trabajo entre diferentes profesionales (veterinarios, recepcionistas, auxiliares).

El proyecto está pensado para que estudiantes de Desarrollo de Aplicaciones Web puedan entender cómo se estructura una aplicación web real, separando claramente la lógica del servidor (backend) de lo que ve el usuario (frontend).

## Arquitectura del Sistema

### Estructura Modular

El proyecto está organizado en módulos para mantener el código ordenado:

```
vetct_web/
├── users/           # Para gestionar usuarios y sus perfiles
├── consultas/       # Para las consultas médicas
├── laboratorio/      # Para los análisis de laboratorio
├── cirugias/        # Para las cirugías programadas
├── urgencias/        # Para los casos de urgencia
└── notificaciones/   # Para el sistema de avisos
```

Cada módulo funciona de forma independiente pero se conecta con el sistema de notificaciones. Así es más fácil mantener y ampliar el código.

## Cómo Funciona la Aplicación

### Parte del Servidor (Backend)

Usamos Django, que es un framework de Python. Django organiza el código en tres partes:

#### Modelos (Datos)
- **¿Qué son?**: Son como planos para guardar información en la base de datos
- **Para qué sirven**: Definen cómo se guardan los usuarios, citas, pacientes, etc.
- **Ejemplo**: Un modelo `Cita` tiene campos como `fecha`, `paciente`, `motivo`

#### Vistas (Lógica)
- **¿Qué son?**: Funciones de Python que procesan lo que pide el usuario
- **Para qué sirven**: Deciden qué mostrar y cómo responder
- **Ejemplo**: Una vista `panel_recepcion` muestra las citas pendientes

#### URLs (Direcciones)
- **¿Qué son?**: Conectan direcciones web con las vistas
- **Para qué sirven**: Definen qué vista se ejecuta para cada URL
- **Ejemplo**: `/notificaciones/recepcion/` ejecuta la vista del panel

### Parte del Cliente (Frontend)

Usamos Tailwind CSS para el diseño y templates de Django para mostrar la información:

#### Templates (Páginas)
- **¿Qué son?**: Archivos HTML que muestran la información
- **Cómo funcionan**: Heredan de una página base para no repetir código
- **Ejemplo**: `panel_recepcion.html` muestra la tabla de citas

#### Estilos (CSS)
- **Tailwind CSS**: Framework que da clases listas para usar
- **Ventajas**: No escribir CSS directamente, solo poner clases
- **Ejemplo**: `class="bg-blue-500 text-white"` hace un botón azul

#### Interactividad (JavaScript)
- **¿Para qué?**: Para hacer la página más dinámica
- **Cómo funciona**: JavaScript básico sin librerías complicadas
- **Ejemplo**: Validar un formulario antes de enviarlo

## Sistema de Usuarios y Permisos

### Tipos de Usuarios

El sistema tiene diferentes tipos de usuarios según su trabajo en la clínica:

- **Cliente**: Son los dueños de las mascotas, piden citas
- **Veterinario**: Son los médicos, atienden las citas
- **Auxiliar**: Ayudan al veterinario en las consultas
- **Recepcionista**: Gestionan las citas que llegan
- **Administrador**: Controla todo el sistema

### Cómo Funcionan los Permisos

Django tiene un sistema de grupos para controlar quién puede hacer qué:

- **Grupos**: Agrupan usuarios por tipo (Veterinarios, Recepcionistas, etc.)
- **Permisos**: Determinan qué puede hacer cada grupo
- **Ejemplo**: Solo los recepcionistas pueden aceptar citas nuevas
- **Ventaja**: Es fácil añadir o quitar permisos sin cambiar el código

## Cómo Funcionan las Notificaciones

El sistema tiene avisos automáticos para que todos sepan lo que pasa:

### Cuando alguien pide una cita

1. Un usuario solicita una cita (consulta, análisis, etc.)
2. Los recepcionistas reciben un aviso automático
3. El aviso aparece en su panel como "pendiente"

### Qué hace el recepcionista

Cuando llega un aviso nuevo, el recepcionista puede:

- **Aceptar**: La cita se confirma y los veterinarios reciben un aviso
- **Rechazar**: La cita se cancela y el aviso se archiva
- **Ver detalles**: Mira toda la información antes de decidir

### Qué hace el veterinario

Cuando el recepcionista acepta una cita:

1. Los veterinarios reciben el aviso
2. El veterinario puede aceptar la cita para asignársela
3. Si no quiere, la cita queda disponible para otros veterinarios
4. Si ya la tenía y quiere cancelarla, vuelve a "pendiente"

### Ventaja del sistema

- **Sin confusión**: Cada uno sabe qué tiene que hacer
- **Orden**: Las citas se mueven automáticamente entre estados
- **Historial**: Queda registro de quién hizo qué y cuándo

## Modelos de Datos Importantes

### Modelo de Notificación

Una notificación es un aviso que se guarda en la base de datos:

```python
class Notificacion(models.Model):
    tipo = models.CharField(max_length=20)  # Puede ser: consulta, analisis, cirugia, urgencia
    objeto_id = models.PositiveIntegerField()  # ID de la cita relacionada
    emisor = models.ForeignKey(User, related_name='enviadas')  # Quien envía el aviso
    receptor = models.ForeignKey(User, related_name='recibidas')  # Quien recibe el aviso
    estado = models.CharField(max_length=20)  # Puede ser: pendiente, aceptada, rechazada
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Cuándo se creó
```

### Estados de una Cita

Las citas pueden estar en tres estados:

- **Pendiente**: Nueva cita, esperando que la acepten
- **Aceptada**: Cita confirmada y asignada a alguien
- **Rechazada**: Cita cancelada o denegada

### Por qué es importante esto

- **Orden**: Cada cita sabe en qué punto está
- **Control**: No se pueden hacer cosas que no tocan
- **Historial**: Se puede ver qué pasó con cada cita

## Páginas Principales del Sistema

### Panel de Recepción

Esta es la página principal para los recepcionistas:

- **Dirección**: `/notificaciones/recepcion/`
- **Qué muestra**: Todas las citas nuevas que llegan
- **Qué puede hacer**: 
  - Ver los detalles de cada cita
  - Aceptar o rechazar las citas
  - Buscar por tipo de servicio
  - La página se adapta al móvil

### Panel de Veterinario

Esta es la página para los veterinarios:

- **Dirección**: `/notificaciones/veterinario/`
- **Qué muestra**: Las citas que tienen asignadas
- **Qué puede hacer**:
  - Ver información completa de sus citas
  - Organizar por pestañas (consultas, análisis, etc.)
  - Cancelar citas si es necesario
  - Interfaz fácil de usar

### Página de Detalles de Cita

Esta página muestra toda la información de una cita:

- **Dirección**: `/notificaciones/ver/<tipo>/<cita_id>/`
- **Qué muestra**: 
  - Datos del paciente
  - Fecha y hora
  - Motivo o tipo de procedimiento
  - Botones para aceptar, rechazar o cancelar

## Cómo Está Hecho el Proyecto

### Organización de Archivos

El proyecto Django tiene esta estructura:

```
vetct_web/
├── manage.py              # Para ejecutar comandos de Django
├── requirements.txt       # Lista de librerías que necesitamos
├── vetct_web/           # Configuración principal
│   ├── settings.py       # Configuración de la aplicación
│   └── urls.py          # URLs principales del sitio
└── apps/               # Las aplicaciones del sistema
    ├── users/           # Para usuarios y login
    ├── consultas/       # Para las consultas
    ├── laboratorio/      # Para los análisis
    ├── cirugias/        # Para las cirugías
    ├── urgencias/        # Para las urgencias
    └── notificaciones/  # Para los avisos
```

### Configuración Básica

- **Base de datos**: SQLite para desarrollo, PostgreSQL para producción
- **Apps instaladas**: Todas las aplicaciones que usamos
- **Middleware**: Seguridad, sesiones, control de usuarios
- **Templates**: Dónde están los archivos HTML
- **Archivos estáticos**: Dónde guardamos CSS, JS, imágenes

### Sistema de Usuarios

- **User extendido**: Añadimos perfil y roles al usuario de Django
- **Grupos**: Agrupamos usuarios por tipo de trabajo
- **Permisos**: Controlamos qué puede hacer cada grupo
- **Decoradores**: Protegemos páginas según el rol

### Páginas Web (Templates)

Así organizamos las páginas:

```
templates/
├── base.html              # Plantilla base que usan todas
├── includes/              # Trozos de código reutilizables
│   ├── header.html        # Menú de navegación
│   └── footer.html        # Pie de página
├── users/                # Páginas de usuarios
├── notificaciones/        # Páginas del sistema de avisos
└── errors/               # Páginas de error (404, 500, etc.)
```

### Estilos con Tailwind

- **Ventaja**: Clases ya hechas, no escribir CSS
- **Organización**: Componentes reutilizables
- **Responsive**: Fácil adaptar a móviles
- **Mantenimiento**: Código más limpio y ordenado

### Diseño para Móviles y Tablets

La web se adapta a diferentes tamaños de pantalla:

#### Puntos de Cambio (Breakpoints)
- **Móvil**: Menos de 640px (todo en una columna)
- **Tablet pequeña**: 640px a 768px (dos columnas)
- **Tablet grande**: 768px a 1024px (layout intermedio)
- **Ordenador**: Más de 1024px (múltiples columnas)

#### Ejemplos de Adaptación

Para tablas que no caben en móvil:

```html
<div class="overflow-x-auto">
    <table class="w-full min-w-[400px]">
        <!-- La tabla se puede mover horizontalmente -->
    </table>
</div>
```

Para layouts que cambian según pantalla:

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- 1 columna en móvil, 2 en tablet, 3 en ordenador -->
</div>
```

Para botones que se apilan en móvil:

```html
<div class="flex flex-col sm:flex-row gap-2">
    <button class="bg-blue-500 text-white px-4 py-2">
        Botón principal
    </button>
</div>
```

## Problemas que Solucionamos

### 1. Errores con Fechas

**El problema**: Al mostrar fechas, dábamos error porque algunos campos solo tenían día y mes, no hora.

**La solución**: Cambiamos el formato en todas las páginas de `|date:"d/m/Y H:i"` a `|date:"d/m/Y"`.

### 2. Avisos Repetidos

**El problema**: Cuando un veterinario aceptaba una cita, se creaba otro aviso nuevo.

**La solución**: Quitamos el código que creaba avisos repetidos en la función de aceptar.

### 3. Estados no se Actualizaban

**El problema**: Al aceptar o rechazar una cita, el aviso seguía apareciendo como "nuevo".

**La solución**: Hicimos que las vistas del recepcionista actualicen también el estado del aviso.

### 4. Faltaban URLs

**El problema**: Las funciones para aceptar/rechazar desde recepción existían pero no tenían dirección web.

**La solución**: Añadimos las URLs `aceptar-recepcion` y `rechazar-recepcion`.

## Cómo se Conectan Frontend y Backend

### Templates de Django

Django conecta el Python con el HTML:

- **Variables globales**: Datos disponibles en todas las páginas
- **Funciones personalizadas**: Pequeñas utilidades para los templates
- **Herencia**: Las páginas heredan de una base común
- **Filtros**: Para formatear datos (fechas, textos, etc.)

### Formularios

Los formularios funcionan así:

- **Validación Python**: Django comprueba que los datos son correctos
- **Seguridad CSRF**: Protección contra ataques
- **Errores**: Django muestra mensajes si algo falla
- **JavaScript**: Validación rápida antes de enviar

### Tecnologías que Usamos

#### Para el Servidor (Backend)
- **Python 3.14**: Lenguaje de programación
- **Django 6.0**: Framework web que organiza todo
- **SQLite**: Base de datos para desarrollo
- **PostgreSQL**: Base de datos para producción
- **Django ORM**: Para hablar con la base de datos sin SQL

#### Para el Navegador (Frontend)
- **HTML5**: Estructura de las páginas
- **Tailwind CSS**: Clases ya hechas para estilos
- **JavaScript**: Para hacer las páginas más dinámicas
- **CSS Grid/Flexbox**: Para organizar los layouts

#### Herramientas de Desarrollo
- **Pip**: Para instalar librerías Python
- **Entorno Virtual**: Para aislar el proyecto
- **Comandos Django**: Para tareas administrativas
- **Archivos Estáticos**: Para CSS, JS, imágenes

## Archivos Principales que Modificamos

### Código del Servidor (Python)

- `notificaciones/views.py`: Toda la lógica de las notificaciones
- `consultas/views.py`: Arreglamos nombres de grupos de usuarios
- `laboratorio/models.py`: Añadimos campo de hora a los análisis
- `users/models.py`: Extendimos el usuario de Django con nuestro perfil
- `users/signals.py`: Automatizamos la asignación de roles

### Páginas Web (HTML)

- `templates/base.html`: La página base que usan todas
- `templates/notificaciones/panel_recepcion.html`: Panel de recepción
- `templates/notificaciones/panel_veterinario.html`: Panel de veterinarios
- `templates/notificaciones/ver_cita.html`: Página de detalles de cita
- `templates/users/mis_citas.html`: Citas del usuario logueado
- `templates/includes/`: Trozos de código reutilizables

### Configuración

- `notificaciones/urls.py`: Direcciones web del sistema
- `vetct_web/settings.py`: Configuración principal de Django
- `requirements.txt`: Librerías que necesita el proyecto

### Comandos Útiles

- `hacer_veterinario.py`: Para hacer usuario veterinario
- `configurar_grupos_notificaciones.py`: Para configurar el sistema

## Comandos Importantes de Django

### Para Configurar el Sistema

```bash
# Hacer que un usuario sea veterinario
python manage.py hacer_veterinario nombre_usuario

# Crear los grupos y permisos
python manage.py configurar_grupos_notificaciones
```

### Para la Base de Datos

```bash
# Crear archivos para cambiar la base de datos
python manage.py makemigrations

# Aplicar los cambios a la base de datos
python manage.py migrate
```

## Cómo Funciona el Sistema en la Práctica

1. **Un cliente pide cita**: Llena un formulario en la web
2. **Los recepcionistas reciben aviso**: Les aparece una notificación
3. **El recepcionista decide**: Acepta o rechaza la cita
4. **Si acepta**: Los veterinarios reciben el aviso
5. **El veterinario acepta**: La cita queda asignada a él
6. **Todo queda registrado**: Se puede ver quién hizo qué y cuándo

## Lo que Consiguiemos Hacer

### Sistema de Avisos Automático
- **Sin tener que recordar nada**: El sistema avisa solo
- **Cada uno recibe sus avisos**: Según su trabajo
- **Las citas se mueven solas**: De pendientes a aceptadas
- **Siempre actualizado**: La información está siempre al día

### Control de Usuarios
- **Cada tipo ve lo suyo**: Clientes, veterinarios, etc.
- **Fácil de gestionar**: Con grupos de Django
- **Seguridad**: Solo pueden hacer lo que corresponde
- **Páginas diferentes**: Según el rol del usuario

### Web que Funciona en Móviles
- **Se ve bien en el móvil**: Las tablas se pueden mover
- **Botones se adaptan**: Se apilan si la pantalla es pequeña
- **Todo usable**: Tanto en ordenador como en móvil
- **Mismo diseño**: Consistente en todos los dispositivos

### Control de Citas
- **Estados claros**: Pendiente, Aceptada, Rechazada
- **No se pueden hacer cosas raras**: Solo cambiar estados válidos
- **Historial completo**: Se ve todo lo que pasó
- **Orden en todo momento**: Sabemos qué está pasando

## La Web en Móviles y Tablets

### Cómo se Adapta la Página

- **Móvil (< 640px)**: Todo en una columna, botones apilados
- **Tablet (640px - 768px)**: Dos columnas, layout adaptado
- **Ordenador (> 768px)**: Múltiples columnas, diseño completo

### Lo que Hicimos para Móviles

- **Tablas con scroll**: Para que no se rompan en pantallas pequeñas
- **Botones que se apilan**: En móvil van uno debajo del otro
- **Textos más pequeños**: Para que quepan mejor
- **Menús adaptativos**: Cambian según el tamaño de pantalla

## Para Siguientes Alumnos

### Ideas para Mejorar el Proyecto

1. **Avisos en tiempo real**: Con WebSocket para no tener que recargar
2. **Calendario visual**: Para ver las citas en un calendario
3. **Historial médico**: Para ver todo el tratamiento de cada mascota
4. **Estadísticas**: Gráficos de cuántas citas hay, etc.
5. **Emails y SMS**: Para recordar las citas a los clientes

### Mejoras Técnicas

1. **Pruebas automáticas**: Para asegurarse de que todo funciona
2. **Docker**: Para que sea fácil desplegarlo
3. **Más velocidad**: Con caching para que vaya más rápido
4. **Mejor organización**: Con más testing y código más limpio

## Evidencias Visuales del Sistema

A continuación se muestran las principales interfaces del sistema VetCT con capturas reales del programa en funcionamiento:

### Panel de Recepción

El panel principal para los recepcionistas donde gestionan todas las citas nuevas:

![Panel de Recepción](images/panel_recepcion.png)

**Características principales implementadas:**
- **Notificaciones recientes**: Lista de avisos pendientes con botones de acción directa
- **Tablas organizadas**: Separadas por estado (pendientes, aceptadas, rechazadas)
- **Diseño adaptativo**: Totalmente funcional en móviles y tablets
- **Contador visual**: Indicador de notificaciones nuevas en tiempo real
- **Acciones rápidas**: Botones Aceptar/Rechazar sin cambiar de página

### Panel Veterinario

Interfaz para los veterinarios donde gestionan sus citas asignadas:

![Panel Veterinario](images/panel_veterinario.png)

**Elementos destacados:**
- **Pestañas organizadas**: Separación clara por tipo de cita (Consultas, Análisis, Cirugías, Urgencias)
- **Estadísticas visuales**: Contadores automáticos de citas por estado
- **Tablas detalladas**: Información completa de cada cita asignada
- **Botones de acción**: Ver detalles, cancelar asignación
- **Filtros funcionales**: Búsqueda y organización por fechas

### Vista de Detalles de Cita

Página completa con toda la información de una cita específica:

![Detalles de Cita](images/ver_cita.png)

**Información mostrada:**
- **Datos del paciente**: Nombre completo, especie, raza, edad
- **Fecha y hora**: Formato claro y legible
- **Motivo o procedimiento**: Descripción detallada del servicio
- **Botones contextuales**: Aceptar, Rechazar, Cancelar según estado
- **Diseño responsive**: Perfecta visualización en cualquier dispositivo
- **Historial de cambios**: Registro de quién modificó qué y cuándo

### Interfaz de Usuario Cliente

Panel principal para los clientes donde gestionan sus propias citas:

![Panel de Usuario](images/panel_usuario.png)

**Funcionalidades disponibles:**
- **Listado personal**: Todas las citas del usuario logueado
- **Filtros avanzados**: Por tipo, estado, fecha
- **Creación de citas**: Formularios intuitivos para solicitar servicios
- **Vista optimizada**: Adaptada completamente para dispositivos móviles
- **Estado en tiempo real**: Actualización automática de estados de citas

### Diseño Responsivo en Acción

Ejemplos reales de cómo se adapta la interfaz a diferentes dispositivos:

![Diseño Responsivo](images/responsive_design.png)

**Adaptaciones implementadas:**
- **Versión móvil (<640px)**: Elementos apilados verticalmente, botones grandes
- **Versión tablet (640px-768px)**: Layout de dos columnas, elementos optimizados
- **Versión escritorio (>768px)**: Múltiples columnas, aprovechamiento completo del espacio
- **Tablas con scroll**: Horizontal en pantallas pequeñas para mantener legibilidad
- **Menús adaptativos**: Navegación que cambia según tamaño de pantalla
- **Textos escalables**: Tamaño de letra que se ajusta automáticamente

---

**Proyecto terminado**: Mayo 2026  
**Versión**: 1.0  
**Tecnologías**: Django 6.0 + Tailwind CSS + Python 3.14
