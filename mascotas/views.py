from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Mascota
from datetime import datetime, date

@login_required
def historial_clinico(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Recopilar todos los eventos médicos
    eventos = []
    
    for c in mascota.consultas.all():
        eventos.append({'tipo': 'Consulta', 'fecha': c.fecha, 'detalle': c.motivo, 'estado': c.estado, 'icono': 'fa-stethoscope', 'color': 'primary'})
        
    for u in mascota.urgencias.all():
        eventos.append({'tipo': 'Urgencia', 'fecha': u.fecha, 'detalle': u.descripcion, 'estado': u.estado, 'icono': 'fa-ambulance', 'color': 'danger'})
        
    for c in mascota.cirugias.all():
        eventos.append({'tipo': 'Cirugía', 'fecha': c.fecha, 'detalle': c.tipo_cirugia, 'estado': c.estado, 'icono': 'fa-procedures', 'color': 'warning'})
        
    for a in mascota.analisis.all():
        # datetime needs to combine date and time to sort properly if others are datetime
        from datetime import datetime, time
        fecha_completa = datetime.combine(a.fecha, a.hora) if hasattr(a, 'hora') else datetime.combine(a.fecha, time())
        eventos.append({'tipo': 'Análisis Lab.', 'fecha': fecha_completa, 'detalle': a.nombre, 'estado': a.estado, 'icono': 'fa-microscope', 'color': 'info'})
        
    for v in mascota.vacunas.all():
        from datetime import datetime, time
        fecha_completa = datetime.combine(v.fecha_aplicacion, time())
        eventos.append({'tipo': 'Vacuna', 'fecha': fecha_completa, 'detalle': v.nombre, 'estado': 'Completado', 'icono': 'fa-syringe', 'color': 'success'})
        
    # Ordenar por fecha descendente (más reciente primero)
    eventos.sort(key=lambda x: x['fecha'], reverse=True)
    
    context = {
        'mascota': mascota,
        'eventos': eventos
    }
    return render(request, 'mascotas/historial.html', context)
