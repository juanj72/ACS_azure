from django.shortcuts import render
from aplicacion.models import *

# Create your views here.

def inicio (request):
    productos=models.producto.objects.all()
    


    return render(request,"index.html",{"productos":productos})


def clientes(request):
    clientesp=cliente.objects.all()
    data={
        'cliente':clientesp
    }
    return render(request,"clientes.html",data)