from django.shortcuts import render
from aplicacion import models

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