from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import calendar

from consultas.models import Consulta
from urgencias.models import Urgencia
from cirugias.models import Cirugia
from laboratorio.models import Analisis

def es_admin(user):
    return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'admin')

@user_passes_test(es_admin)
def dashboard_analitico(request):
    hoy = timezone.now()
    
    # mascotas atendidas (consultas) de este mes frente al anterior
    primer_dia_mes_actual = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ultimo_dia_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
    primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    consultas_este_mes = Consulta.objects.filter(fecha__gte=primer_dia_mes_actual).count()
    consultas_mes_anterior = Consulta.objects.filter(fecha__gte=primer_dia_mes_anterior, fecha__lt=primer_dia_mes_actual).count()
    
    # servicios rentables (me lo invento un poco con precios base)
    vol_cirugias = Cirugia.objects.all().count()
    vol_consultas = Consulta.objects.all().count()
    vol_urgencias = Urgencia.objects.all().count()
    vol_analisis = Analisis.objects.all().count()
    
    # Precios simulados
    rentabilidad = {
        'Cirugías': vol_cirugias * 250,
        'Consultas': vol_consultas * 40,
        'Urgencias': vol_urgencias * 80,
        'Laboratorio': vol_analisis * 60
    }
    
    # calculo de urgencias por la noche (20:00 a 08:00)
    total_urgencias = Urgencia.objects.count()
    if total_urgencias > 0:
        urgencias_nocturnas = Urgencia.objects.filter(fecha__hour__gte=20).count() + Urgencia.objects.filter(fecha__hour__lt=8).count()
        pct_nocturnas = (urgencias_nocturnas / total_urgencias) * 100
        pct_diurnas = 100 - pct_nocturnas
    else:
        pct_nocturnas, pct_diurnas = 0, 0
        urgencias_nocturnas = 0
        
    # historial de atenciones de los ultimos 6 meses para la grafica
    labels_meses = []
    datos_evolucion = []
    for i in range(5, -1, -1):
        d = hoy - timedelta(days=i*30)
        labels_meses.append(d.strftime('%b'))
        inicio_mes = d.replace(day=1, hour=0, minute=0, second=0)
        _, num_days = calendar.monthrange(inicio_mes.year, inicio_mes.month)
        fin_mes = inicio_mes.replace(day=num_days, hour=23, minute=59, second=59)
        
        c = Consulta.objects.filter(fecha__range=(inicio_mes, fin_mes)).count()
        datos_evolucion.append(c)

    context = {
        'mes_actual': consultas_este_mes,
        'mes_anterior': consultas_mes_anterior,
        'rentabilidad_labels': list(rentabilidad.keys()),
        'rentabilidad_data': list(rentabilidad.values()),
        'pct_nocturnas': round(pct_nocturnas, 1),
        'pct_diurnas': round(pct_diurnas, 1),
        'total_urgencias': total_urgencias,
        'urgencias_nocturnas': urgencias_nocturnas,
        'labels_meses': labels_meses,
        'datos_evolucion': datos_evolucion
    }
    
    return render(request, 'metricas/dashboard.html', context)
