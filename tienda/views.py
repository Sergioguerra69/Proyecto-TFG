# Vistas de la tienda
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Producto

# Pagina de la tienda
def lista_productos(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'tienda/tienda.html', {'productos': productos})

# API REST para productos (devuelve JSON)
def api_productos(request):
    # Sacamos todos los productos de la base de datos
    productos = Producto.objects.all()
    
    # Creamos una lista con los datos
    datos = []
    for p in productos:
        datos.append({
            'id': p.id,
            'nombre': p.nombre,
            'precio': float(p.precio),
            'stock': p.stock,
            'imagen': p.imagen.url if p.imagen else None
        })
    
    # Devolvemos JSON
    return JsonResponse(datos, safe=False)

# Pagina para crear producto nuevo (solo admin)
def nuevo_producto(request):
    # Verificar que es admin
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para crear productos')
        return redirect('tienda')
    
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        
        # Crear el producto
        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock
        )
        
        # Si hay imagen, la guardamos
        if request.FILES.get('imagen'):
            producto.imagen = request.FILES.get('imagen')
        
        producto.save()
        messages.success(request, 'Producto creado correctamente')
        return redirect('tienda')
    
    return render(request, 'tienda/nuevo_producto.html')
