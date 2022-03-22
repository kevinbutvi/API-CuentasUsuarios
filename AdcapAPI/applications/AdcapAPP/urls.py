from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "adcap_app"

cliente = [
    path(
        'registrar/cliente/', 
        views.ClienteCreateAPIView.as_view(),
        name="registrar-cliente"
        ),
    path(
        'update/cliente/<pk>/', 
        views.ClienteRetrieveUpdateAPIView.as_view(),
        name="update-cliente"
        ),
    path(
        'eliminar/cliente/<pk>/', 
        views.ClienteDestroyAPIView.as_view(),
        name="eliminar-cliente"
        ),
    path(
        'detalle/cliente/<pk>/', 
        views.ClienteRetrieveAPIView.as_view(),
        name="detalle-cliente"
        ),
    path(
        'lista/clientes/', 
        views.ClienteListAPIView.as_view(),
        name="lista-clientes"
        ),
    path(
        'lista/clientes-paginados/', 
        views.ClientePAGINATIONListAPIView.as_view(),
        name="lista-clientes-paginados"
        ),
    path(
        'cliente/<pk>', 
        views.ClienteRetrieveUpdateDestroyAPIView.as_view(),
        name="cliente"
        ),
]


movimiento = [
    path(
        'registrar/movimiento/', 
        views.RegistrarMovimientoUpdateAPIView.as_view(),
        name="registrar-movimiento"
        ),
    path(
        'detalle/movimiento/<pk>/', 
        views.DetalleMovimientoPKListAPIView.as_view(),
        name="detalle-movimientoPK"
        ),
    path(
        'eliminar/movimiento/<pk>', 
        views.EliminarMovimientoDetroyAPIView.as_view(),
        name="eliminar-movimientoPK"
        ),
]


saldo = [
    path(
        'detalle/cliente-saldos/', 
        views.ClienteSaldoListAPIView.as_view(),
        name="saldo-clientes"
        ),
    path(
        'detalle/cliente-saldos/<pk>/', 
        views.ClienteSaldoPKListAPIView.as_view(),
        name="saldo-clientesPK"
        ),
]


urlpatterns = cliente + movimiento + saldo
