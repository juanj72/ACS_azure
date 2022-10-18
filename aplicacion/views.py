from django.shortcuts import render,redirect
from aplicacion import models
from aplicacion.forms import Formulario_clientes, Formulario_ventas, Formularioproducto
from django.db import connection
from datetime import date

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



def ventasr(request):
    formulario = Formulario_clientes(request.POST or None)
    #formulario2= Formulario_ventas(request.POST or None)
    muestravent=models.ventas.objects.all()
    #var='hola'
    if request.method=='POST':
     
     if formulario.is_valid:
         formulario.save()
         return redirect('prueba_venta')  

  

    return render(request,"venta.html",{'formulario_cliente':formulario,'ventas':muestravent})



def venta_registro(request):
    #clientes=cliente.objects.all()
    productos=models.producto.objects.all()
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
        productos=models.producto.objects.get(id=request.POST['idProducto'])
        
        
        


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


