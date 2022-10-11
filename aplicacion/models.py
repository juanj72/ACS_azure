from tkinter import CASCADE
from tkinter.tix import INTEGER
from django.db import models

# Create your models here.
class producto(models.Model):
    Nombre_producto=models.CharField(max_length=100)
    valor_neto=models.IntegerField()
    valor_publico=models.IntegerField()
    cantidad=models.IntegerField()
    def __str__(self):
        return self.Nombre_producto
    



class cliente(models.Model):
    Nombre_cliente=models.CharField(max_length=100)
    Documento=models.IntegerField()
    def __str__(self):
        return self.Nombre_cliente



class ventas(models.Model):
    idCliente=models.ForeignKey(cliente, on_delete=models.CASCADE)
    idProducto=models.ForeignKey(producto,on_delete=models.CASCADE)
    fecha_compra=models.DateField(auto_now=True)
    cantidad=models.IntegerField(null=True)
    numero_factura=models.IntegerField(null=True)
   
    
    


class reportes (models.Model):
    numero_factura=models.IntegerField(null=True)
    #def __str__(self):
        #return self.numero_factura       

