# Utilidades para generación de PDFs con Reportlab
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.utils import timezone
from datetime import datetime
import os

class PageNumberCanvas(canvas.Canvas):
    """Canvas personalizado para añadir números de página y pie de página"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
    
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
    
    def save(self):
        page_count = len(self.pages)
        for page_num, page_data in enumerate(self.pages, start=1):
            self.__dict__.update(page_data)
            self.draw_page_number(page_num, page_count)
            self.draw_footer()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    
    def draw_page_number(self, page_num, page_count):
        """Dibuja el número de página"""
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        self.drawRightString(A4[0] - 50, 30, f"Página {page_num} de {page_count}")
    
    def draw_footer(self):
        """Dibuja el pie de página con copyright"""
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.grey)
        self.drawCentredString(A4[0] / 2, 20, "© 2024 VetCT - Centro Veterinario Integral. Todos los derechos reservados.")
        self.drawCentredString(A4[0] / 2, 12, "Colegio Miralmonte, Polígono Santa Ana, Murcia - Tel: +34 722 19 49 81 - atencion@vetct.com")

def generar_pdf_consulta(consulta, response):
    """Genera un PDF para una consulta veterinaria"""
    doc = SimpleDocTemplate(response, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0891b2'),  # cyan-600
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#06b6d4'),  # cyan-500
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=14,
        fontName='Helvetica'
    )
    
    # Header con información de la clínica
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4b5563'),  # gray-600
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Logo placeholder (texto estilizado)
    logo_style = ParagraphStyle(
        'Logo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#06b6d4'),  # cyan-500
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    elements.append(Paragraph("🐾 VetCT", logo_style))
    elements.append(Paragraph("Centro Veterinario Integral", header_style))
    elements.append(Paragraph("Colegio Miralmonte, Polígono Santa Ana, Murcia, España", header_style))
    elements.append(Paragraph("+34 722 19 49 81 | Lun-Sáb: 9:00 - 20:00 | atencion@vetct.com", header_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Línea separadora
    elements.append(Paragraph("_" * 80, ParagraphStyle('Line', parent=styles['Normal'], fontSize=2, textColor=colors.HexColor('#e2e8f0'), alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.3*inch))
    
    # Título del reporte
    elements.append(Paragraph("REPORTE DE CONSULTA VETERINARIA", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Datos del paciente
    data_paciente = [
        ['Paciente:', consulta.paciente or consulta.mascota.nombre if consulta.mascota else 'N/A'],
        ['Tipo de Animal:', consulta.tipo_animal],
        ['Dueño:', consulta.usuario.get_full_name() or consulta.usuario.username],
        ['Fecha de Cita:', consulta.fecha.strftime('%d/%m/%Y %H:%M')],
        ['Estado:', consulta.estado]
    ]
    
    table_paciente = Table(data_paciente, colWidths=[2*inch, 3*inch])
    table_paciente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecfeff')),  # cyan-50
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0891b2')),  # cyan-600
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#cffafe')),  # cyan-100
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),  # slate-200
    ]))
    elements.append(table_paciente)
    elements.append(Spacer(1, 0.3*inch))
    
    # Motivo de la consulta
    elements.append(Paragraph("Motivo de la Consulta", subtitle_style))
    elements.append(Paragraph(consulta.motivo, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Diagnóstico (si existe)
    if consulta.diagnostico:
        elements.append(Paragraph("Diagnóstico Veterinario", subtitle_style))
        elements.append(Paragraph(consulta.diagnostico, normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Veterinario asignado
    if consulta.veterinario:
        elements.append(Paragraph("Veterinario Asignado", subtitle_style))
        elements.append(Paragraph(f"Dr. {consulta.veterinario.get_full_name() or consulta.veterinario.username}", normal_style))
        if hasattr(consulta.veterinario, 'perfil') and consulta.veterinario.perfil.especialidad:
            elements.append(Paragraph(f"Especialidad: {consulta.veterinario.perfil.especialidad}", normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Datos de contacto
    elements.append(Paragraph("Datos de Contacto", subtitle_style))
    contacto_data = [
        ['Teléfono:', consulta.telefono or 'No especificado'],
        ['Email:', consulta.correo or 'No especificado'],
        ['DNI:', consulta.dni or 'No especificado']
    ]
    table_contacto = Table(contacto_data, colWidths=[1.5*inch, 3.5*inch])
    table_contacto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecfeff')),  # cyan-50
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0891b2')),  # cyan-600
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#cffafe')),  # cyan-100
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),  # slate-200
    ]))
    elements.append(table_contacto)
    elements.append(Spacer(1, 0.5*inch))
    
    # Fecha de generación
    elements.append(Paragraph(f"Reporte generado el: {timezone.now().strftime('%d/%m/%Y %H:%M')}", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Usar canvas personalizado para pie de página
    doc.build(elements, canvasmaker=PageNumberCanvas)
    return response

def generar_pdf_cirugia(cirugia, response):
    """Genera un PDF para una cirugía"""
    doc = SimpleDocTemplate(response, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#dc2626'),  # red-600
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#ef4444'),  # red-500
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=14,
        fontName='Helvetica'
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4b5563'),  # gray-600
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    logo_style = ParagraphStyle(
        'Logo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#06b6d4'),  # cyan-500
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    elements.append(Paragraph(" VetCT", logo_style))
    elements.append(Paragraph("Centro Veterinario Integral", header_style))
    elements.append(Paragraph("Colegio Miralmonte, Polígono Santa Ana, Murcia, España", header_style))
    elements.append(Paragraph("+34 722 19 49 81 | Lun-Sáb: 9:00 - 20:00 | atencion@vetct.com", header_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("_" * 80, ParagraphStyle('Line', parent=styles['Normal'], fontSize=2, textColor=colors.HexColor('#e2e8f0'), alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("REPORTE DE CIRUGÍA", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Datos de la cirugía
    data_cirugia = [
        ['Tipo de Cirugía:', cirugia.tipo_cirugia],
        ['Paciente:', cirugia.paciente or cirugia.mascota.nombre if cirugia.mascota else 'N/A'],
        ['Tipo de Animal:', cirugia.tipo_animal],
        ['Dueño:', cirugia.usuario.get_full_name() or cirugia.usuario.username],
        ['Fecha:', cirugia.fecha.strftime('%d/%m/%Y %H:%M')],
        ['Quirófano:', cirugia.quirofano],
        ['Estado:', cirugia.estado]
    ]
    
    table_cirugia = Table(data_cirugia, colWidths=[2*inch, 3*inch])
    table_cirugia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef2f2')),  # red-50
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#dc2626')),  # red-600
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#fee2e2')),  # red-100
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),  # slate-200
    ]))
    elements.append(table_cirugia)
    elements.append(Spacer(1, 0.3*inch))
    
    # Veterinario
    if cirugia.veterinario:
        elements.append(Paragraph("Veterinario Responsable", subtitle_style))
        elements.append(Paragraph(f"Dr. {cirugia.veterinario.get_full_name() or cirugia.veterinario.username}", normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Datos de contacto
    elements.append(Paragraph("Datos de Contacto", subtitle_style))
    contacto_data = [
        ['Teléfono:', cirugia.telefono or 'No especificado'],
        ['Email:', cirugia.correo or 'No especificado'],
        ['DNI:', cirugia.dni or 'No especificado']
    ]
    table_contacto = Table(contacto_data, colWidths=[1.5*inch, 3.5*inch])
    table_contacto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef2f2')),  # red-50
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#dc2626')),  # red-600
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#fee2e2')),  # red-100
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),  # slate-200
    ]))
    elements.append(table_contacto)
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph(f"Reporte generado el: {timezone.now().strftime('%d/%m/%Y %H:%M')}", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)))
    
    doc.build(elements, canvasmaker=PageNumberCanvas)
    return response

def generar_pdf_urgencia(urgencia, response):
    """Genera un PDF para una urgencia"""
    doc = SimpleDocTemplate(response, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#ea580c'),  # orange-600
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#f97316'),  # orange-500
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=14,
        fontName='Helvetica'
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4b5563'),  # gray-600
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    logo_style = ParagraphStyle(
        'Logo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#06b6d4'),  # cyan-500
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    elements.append(Paragraph("🐾 VetCT", logo_style))
    elements.append(Paragraph("Centro Veterinario Integral", header_style))
    elements.append(Paragraph("Colegio Miralmonte, Polígono Santa Ana, Murcia, España", header_style))
    elements.append(Paragraph("+34 722 19 49 81 | Lun-Sáb: 9:00 - 20:00 | atencion@vetct.com", header_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("_" * 80, ParagraphStyle('Line', parent=styles['Normal'], fontSize=2, textColor=colors.HexColor('#e2e8f0'), alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("REPORTE DE URGENCIA", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Datos de la urgencia
    prioridad_color = {
        'Pendiente': colors.grey,
        'Baja': colors.green,
        'Media': colors.yellow,
        'Alta': colors.orange,
        'Crítica': colors.red
    }.get(urgencia.prioridad, colors.grey)
    
    data_urgencia = [
        ['Paciente:', urgencia.paciente or urgencia.mascota.nombre if urgencia.mascota else 'N/A'],
        ['Tipo de Animal:', urgencia.tipo_animal],
        ['Dueño:', urgencia.usuario.get_full_name() or urgencia.usuario.username],
        ['Fecha de Llegada:', urgencia.fecha.strftime('%d/%m/%Y %H:%M')],
        ['Prioridad:', urgencia.prioridad],
        ['Estado:', urgencia.estado],
        ['Solicita Prioridad:', 'Sí' if urgencia.solicita_prioridad else 'No']
    ]
    
    table_urgencia = Table(data_urgencia, colWidths=[2*inch, 3*inch])
    table_urgencia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff7ed')),  # orange-50
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#ea580c')),  # orange-600
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ffedd5')),  # orange-100
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),  # slate-200
    ]))
    elements.append(table_urgencia)
    elements.append(Spacer(1, 0.3*inch))
    
    # Descripción
    elements.append(Paragraph("Descripción del Caso", subtitle_style))
    elements.append(Paragraph(urgencia.descripcion, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Datos de contacto
    elements.append(Paragraph("Datos de Contacto", subtitle_style))
    contacto_data = [
        ['Teléfono:', urgencia.telefono or 'No especificado'],
        ['Email:', urgencia.correo or 'No especificado'],
        ['DNI:', urgencia.dni or 'No especificado']
    ]
    table_contacto = Table(contacto_data, colWidths=[1.5*inch, 3.5*inch])
    table_contacto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff7ed')),  # orange-50
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#ea580c')),  # orange-600
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ffedd5')),  # orange-100
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),  # slate-200
    ]))
    elements.append(table_contacto)
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph(f"Reporte generado el: {timezone.now().strftime('%d/%m/%Y %H:%M')}", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)))
    
    doc.build(elements, canvasmaker=PageNumberCanvas)
    return response
