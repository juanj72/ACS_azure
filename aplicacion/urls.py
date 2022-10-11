from django.urls import path
from .import views


urlpatterns=[
    path('',views.inicio,name='inicio'),
    path('/cliente',views.clientes,name="cliente"),
    path('/verpro',views.ver_producto,name="ver_producto"),
    path('/eliminar/<int:id>',views.eliminarpro,name="eliminar"),
    path('/editar_pro/<int:id>',views.editar,name="modal_editar"),
    path('/venta',views.ventasr,name="venta"),
    path('/reportes',views.reportes,name="reportes"),
    path('/prueba_venta',views.venta_registro, name="prueba_venta"),
    path('/reporfecha',views.fechas,name="fechas"),
    path('/eliminar_venta/<int:id>',views.eliminar_venta,name="eliminar_venta"),
    path('/recibo/<int:factura>',views.recibo,name="recibo"),
    path('/cerrar_sesion',views.cerrar_sesion,name="cerrar_sesion"),
    path('/anular',views.anulacion,name="anular"),
    path('/listado_productos_vent',views.total_productos,name="total_productos_vendidos")
        
    
]