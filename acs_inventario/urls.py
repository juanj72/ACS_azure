"""acs_inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import logout_then_login, LoginView
from aplicacion import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',include('aplicacion.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
     path('',views.inicio,name='inicio'),
    path('cliente',views.clientes,name="cliente"),
    path('verpro',views.ver_producto,name="ver_producto"),
    path('eliminar/<int:id>',views.eliminarpro,name="eliminar"),
    path('editar_pro/<int:id>',views.editar,name="modal_editar"),
    path('venta',views.ventasr,name="venta"),
    path('reportes',views.reportes,name="reportes"),
    path('prueba_venta',views.venta_registro, name="prueba_venta"),
    path('reporfecha',views.fechas,name="fechas"),
    path('eliminar_venta/<int:id>',views.eliminar_venta,name="eliminar_venta"),
    path('recibo/<int:factura>',views.recibo,name="recibo"),
    path('cerrar_sesion',views.cerrar_sesion,name="cerrar_sesion"),
    path('anular',views.anulacion,name="anular"),
    path('listado_productos_vent',views.total_productos,name="total_productos_vendidos")
]


urlpatterns += staticfiles_urlpatterns()
