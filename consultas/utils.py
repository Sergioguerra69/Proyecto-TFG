import datetime
from datetime import timedelta

def fecha_hora_disponible(fecha_dt, exclude_model=None, exclude_id=None):
    """
    Verifica si una fecha y hora están disponibles en el calendario general de la clínica,
    comprobando colisiones con Consultas, Cirugías, Estética, Análisis y Formularios de Contacto.
    Se considera un margen de 29 minutos para evitar solapamientos.
    """
    inicio = fecha_dt - timedelta(minutes=29)
    fin = fecha_dt + timedelta(minutes=29)
    
    # 1. Verificar en Consulta
    from consultas.models import Consulta
    qs_consultas = Consulta.objects.filter(fecha__range=(inicio, fin))
    if exclude_model == 'Consulta' and exclude_id:
        qs_consultas = qs_consultas.exclude(id=exclude_id)
    if qs_consultas.exists():
        return False
        
    # 2. Verificar en Cirugia
    from cirugias.models import Cirugia
    qs_cirugias = Cirugia.objects.filter(fecha__range=(inicio, fin))
    if exclude_model == 'Cirugia' and exclude_id:
        qs_cirugias = qs_cirugias.exclude(id=exclude_id)
    if qs_cirugias.exists():
        return False

    # 3. Verificar en ServicioEstetica
    from estetica.models import ServicioEstetica
    qs_estetica = ServicioEstetica.objects.filter(fecha__range=(inicio, fin))
    if exclude_model == 'ServicioEstetica' and exclude_id:
        qs_estetica = qs_estetica.exclude(id=exclude_id)
    if qs_estetica.exists():
        return False

    # 4. Verificar en Analisis (fecha DateField, hora TimeField)
    from laboratorio.models import Analisis
    qs_analisis = Analisis.objects.filter(fecha=fecha_dt.date())
    if exclude_model == 'Analisis' and exclude_id:
        qs_analisis = qs_analisis.exclude(id=exclude_id)
    for a in qs_analisis:
        if a.hora:
            dt_a = datetime.datetime.combine(a.fecha, a.hora)
            if inicio <= dt_a <= fin:
                return False

    # 5. Verificar en FormularioContacto (fecha DateField, hora TimeField)
    from contacto.models import FormularioContacto
    qs_contacto = FormularioContacto.objects.filter(fecha=fecha_dt.date())
    if exclude_model == 'FormularioContacto' and exclude_id:
        qs_contacto = qs_contacto.exclude(id=exclude_id)
    for c in qs_contacto:
        if c.hora:
            dt_c = datetime.datetime.combine(c.fecha, c.hora)
            if inicio <= dt_c <= fin:
                return False

    return True
