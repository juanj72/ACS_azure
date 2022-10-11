
from audioop import add
from datetime import date
from operator import index
from sqlite3 import Cursor
from unicodedata import name
from warnings import catch_warnings
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from aplicacion.forms import Formulario_clientes, Formulario_ventas, Formularioproducto
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest
from django.contrib.auth import logout

# Create your views here.

@login_required
def inicio(request):

       with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute('select distinct numero_factura from aplicacion_reportes')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()
        print(data)

        arr_report=[]
        arr_ventas=[]
        arr_sinrep=[]
        mensaje=None
        for i in range(len(data)):
         arr_report.append(data[i]['numero_factura'])
        
        for b in range(len(ver_ventas())):
            arr_ventas.append(ver_ventas()[b]['numero_factura'])

        #print(arr_report)
        print('facturas en ventas')
        #print(arr_ventas)

        for z in range(len(arr_ventas)):
            if arr_ventas[z] not in arr_report:
                arr_sinrep.append(arr_ventas[z])
        
        print(arr_sinrep)

        if len(arr_sinrep)!=0:
            mensaje=True


       
    
        return render(request,"./index.html",{"mensaje":mensaje,"recibos":arr_sinrep})




def ver_ventas():
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute('select distinct numero_factura from aplicacion_ventas')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

        return(data)
 



@login_required
def clientes(request):
    clientesp=cliente.objects.all()
    data={
        'cliente':clientesp
    }
    return render(request,"clientes.html",data)


@login_required
def ver_producto(request):
    productopy=producto.objects.all()
    
    formulario = Formularioproducto(request.POST or None)
    if request.method=='POST':
     
     if formulario.is_valid:
         formulario.save()
         return redirect('ver_producto')
    
    return render(request,"verpro.html",{'formulario':formulario,'productos':productopy})




@login_required
def eliminarpro(request,id):
    pro=producto.objects.get(id=id)
    pro.delete()
    return redirect('ver_producto')







@login_required
def editar(request, id):
    productopy=producto.objects.get(id=id)
    formulario=Formularioproducto(request.POST or None, instance=productopy)
    if formulario.is_valid and request.method=='POST':
        formulario.save()
        return redirect('ver_producto')
    return render(request,"modaleditarpro.html",{'formulario':formulario})



@login_required
def ventasr(request):
    formulario = Formulario_clientes(request.POST or None)
    #formulario2= Formulario_ventas(request.POST or None)
    muestravent=ventas.objects.all()
    #var='hola'
    if request.method=='POST':
     
     if formulario.is_valid:
         formulario.save()
         return redirect('prueba_venta')  

  

    return render(request,"venta.html",{'formulario_cliente':formulario,'ventas':muestravent})



@login_required
def reportes(request):
    #ventar=ventas.objects.values()
    
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute('call Reportes()')

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()


    return render(request,"reportes.html",{'reportes':data})






@login_required
def venta_registro(request):
    #clientes=cliente.objects.all()
    productos=producto.objects.all()
    formulario=Formulario_ventas(request.POST or None)
    mensaje_cantidad=False
    mensaje_agregado=False
    reporte=ver_reportes()
    arr_report=[]
    for i in range(len(reporte)):
        arr_report.append(reporte[i]['numero_factura'])

    factura_repetida=None
    carro=None
    total=None
    factura=None

    if request.POST.get('idCliente') and request.POST.get('idProducto')and request.POST.get('cantidad') and request.POST.get('numero_factura') and int(request.POST['numero_factura']) not in arr_report:
        productos=producto.objects.get(id=request.POST['idProducto'])
        
        
        


        if productos.cantidad<int(request.POST['cantidad']) or int(request.POST['cantidad'])<=0:
            mensaje_cantidad=True

        else:
           
            var1=request.POST['idCliente']
            print(var1)
            formulario.save()
            mensaje_agregado=True            
            factura=request.POST['numero_factura']
        carro=carrito(request.POST['numero_factura'])
        total=total_carrito(request.POST['numero_factura'])
        
        if factura!=None:
            mensaje_agregado=True
    else:
        factura_repetida=True

                

    return render(request,"pruebaventa.html",{"factura_repetida":factura_repetida,"formulario":formulario,"error_cantidad":mensaje_cantidad,"mensaje_agregado":mensaje_agregado,"carro":carro,"total":total,"factura_no":mensaje_agregado,"factura":factura})

@login_required
def eliminar_venta(request,id):
 vent=ventas.objects.filter(numero_factura=id) 
 vent.delete()
 return redirect('prueba_venta')





def ver_reportes():
      with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute('call ver_reportes()')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

      return (data)
    







def carrito(factura):

    
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(f'call factura_actual({factura})')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

    return (data)



def total_carrito(factura):

     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(f'call total_venta({factura})')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

     return (data)


















@login_required
def fechas(request):
    #fecha=request.POST['fecha']
    
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD

        if 'fecha' in request.POST:
            fecha=request.POST['fecha']
            print(fecha)
            


        else:
            fecha=date.today()
            #total=total_fecha('2022-09-15')


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(f'call reporte_fecha(\'{fecha}\')')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

        #print(data)


    with connection.cursor() as cursor2:  # Activamos un cursor para las consultas a la BD

         if 'fecha' in request.POST:
            fecha2=request.POST['fecha']
            print(fecha2)
            


         else:
            fecha2=date.today()
            #total=total_fecha('2022-09-15')


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
         cursor2.execute(f'call total_ventas_diarias(\'{fecha2}\')')
        #total=total_fecha(fecha)

         columns2 = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
         for column2 in cursor2.description:

            columns2.append(column2[0])  # Guardando el nombre de las columnas

         data2 = []  # Lista con los datos que vamos a enviar en JSON

         for row2 in cursor2.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data2.append(dict(zip(columns2, row2)))

         cursor2.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

         connection.commit()  # Enviamos la sentencia a la BD
         connection.close()

         print(data2)   


    return render(request,"reporfecha.html",{'reporte':data,'total':data2})



def add_reporte(factura):
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(f'call add_reporte({factura})')
        #total=total_fecha(fecha)

       

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

     pass





@login_required
def recibo(request,factura):
    add_reporte(factura)
    total_venta2=total_carrito(factura)
    datos_venta1=carrito(factura)
    

   

    

    return render(request,'recibo.html',{"total":total_venta2,"datos":datos_venta1})



def cerrar_sesion(request):

    logout(request)

    return redirect('/')


@login_required
def anulacion(request):
      
       with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute('select distinct numero_factura from aplicacion_reportes')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()


        mensaje_hecho=None 
        if request.POST.get('anular'):

            print(request.POST['anular'])
            anular_venta(request.POST['anular'])
            mensaje_hecho=True
    

        return render(request,"anular.html",{"recibo":data,"exito":mensaje_hecho})


def anular_venta(numero_factura):
    vent=ventas.objects.filter(numero_factura=numero_factura)
    vent.delete()
    anular_recibo(numero_factura)
    
    
    pass 


def anular_recibo(numero_factura):
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(f'delete from aplicacion_reportes where numero_factura={numero_factura}')
        #total=total_fecha(fecha)

       

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()
     pass


def listado_productos():
    
       with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    


        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute('call listado_productos_vendidos')
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

        return(data)






def total_productos(request):
    total_prod=listado_productos()

    return render(request,"cantidad_producto_vendido.html",{"reporte":total_prod})
