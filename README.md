# VetCT - Proyecto Final de Grado (DAW 2026)

## Descripción
VetCT es un sistema integral de gestión para clínicas veterinarias, desarrollado como Proyecto Final de Grado. El sistema permite la gestión de pacientes, citas, suministros médicos y servicios especializados.

## Módulos
El proyecto está estructurado de forma modular para facilitar su escalabilidad y mantenimiento:

*   **Gestión de Consultas:** Registro y seguimiento de visitas clínicas generales.
*   **Laboratorio Clínico:** Gestión de análisis, resultados y pruebas diagnósticas.
*   **Urgencias 24h:** Triaje y atención inmediata con sistema de prioridades.
*   **Estética Veterinaria:** Agenda para servicios de peluquería y cuidado estético.
*   **Quirófano (Cirugías):** Control de intervenciones quirúrgicas y estado de quirófanos (Acceso restringido a administradores).
*   **Tienda Online:** Catálogo de suministros y productos para mascotas.

## Tecnologías Utilizadas
*   **Backend:** Django 5.1.6, Django Rest Framework (API), Django Channels (Websockets).
*   **Frontend:** Bootstrap 5, HTML5 Semántico.
*   **Infraestructura:** Docker, Docker-Compose, Nginx (Proxy Inverso), Redis (Caché y Mensajería).
*   **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Producción).

## Despliegue con Docker
Para arrancar el proyecto en un entorno de producción o desarrollo académico:

```bash
docker-compose up --build
```

## API Endpoints
Para cumplir con los estándares de interoperabilidad, el sistema ofrece una API REST desarrollada con **Django Rest Framework (DRF)**:

*   **Listar Servicios:** `GET /api/servicios/` - Devuelve la cartera de servicios en formato JSON.

El sistema estará disponible en `http://localhost`.