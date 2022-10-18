from django.shortcuts import render,redirect
from aplicacion import models
from aplicacion.forms import Formulario_clientes, Formulario_ventas, Formularioproducto

# Create your views here.

def inicio (request):
    productos=models.producto.objects.all()
    


    return render(request,"index.html",{"productos":productos})


def clientes(request):
    clientesp=models.cliente.objects.all()
    data={
        'cliente':clientesp
    }
    return render(request,"clientes.html",data)


def ver_producto(request):
    productopy=models.producto.objects.all()
    
    formulario = Formularioproducto(request.POST or None)
    if request.method=='POST':
     
     if formulario.is_valid:
         formulario.save()
         return redirect('ver_producto')
    
    return render(request,"verpro.html",{'formulario':formulario,'productos':productopy})



def eliminarpro(request,id):
    pro=models.producto.objects.get(id=id)
    pro.delete()
    return redirect('ver_producto')








def editar(request, id):
    productopy=models.producto.objects.get(id=id)
    formulario=Formularioproducto(request.POST or None, instance=productopy)
    if formulario.is_valid and request.method=='POST':
        formulario.save()
        return redirect('ver_producto')
    return render(request,"modaleditarpro.html",{'formulario':formulario})