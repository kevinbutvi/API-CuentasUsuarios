from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
    )


from .models import (
    Cliente,
    Movimiento,
    MovimientoDetalle,
    Cuenta,
    )

from .serializers import (
    ClienteSerializer,
    Paginador,
    MovimientoDetalleSerializer,
    MovimientoSerializer,
    ClienteSaldoSerializer,
    RegistrarMovimientoSerializer,
    EliminaMovimientoSerializer,
    ClienteSaldoUSDSerializer,
    )

from rest_framework import status
from rest_framework.response import Response
from django.http import Http404




# CLIENTES 

class ClienteCreateAPIView(CreateAPIView):
    """ Creacion de Cliente """
    
    serializer_class = ClienteSerializer
    

class ClienteRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """ Update de Cliente por PK"""
    
    serializer_class = ClienteSerializer
    queryset = Cliente


class ClienteDestroyAPIView(RetrieveDestroyAPIView):
    """ Eliminar un cliente por PK """
    
    serializer_class = ClienteSerializer
    queryset = Cliente


class ClienteRetrieveAPIView(RetrieveAPIView):
    """ Mostrar Detalles de un Cliente """
    
    serializer_class = ClienteSerializer
    queryset = Cliente


class ClienteRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """ Muestra, Edita o Elimina Cliente en 1 sola View """
    serializer_class = ClienteSerializer
    queryset = Cliente
    

class ClienteListAPIView(ListAPIView):
    """ Mostrar TODOS los Clientes SIN Paginacion """
    
    serializer_class = ClienteSerializer

    def get_queryset(self):
        return (Cliente.objects.all())


class ClientePAGINATIONListAPIView(ListAPIView):
    """ Mostrar TODOS los Cliente CON Paginacion """
    
    serializer_class = ClienteSerializer
    pagination_class = Paginador

    def get_queryset(self):
        return (Cliente.objects.all())


# SALDO

class ClienteSaldoListAPIView(ListAPIView):
    """ Listado de Clientes y sus Saldos """
    
    serializer_class = ClienteSaldoSerializer

    def get_queryset(self):
        return (Cuenta.objects.all())


class ClienteSaldoPKListAPIView(ListAPIView):
    """ Devuelve saldo para cliente en particular """
    
    serializer_class = ClienteSaldoUSDSerializer
    
    def get_queryset(self, **kwargs):
        """ Manipulo la PK que se envia por URL y la mando al manager para realizar filtro"""
        clave = self.kwargs["pk"]
        return (Cuenta.objects.saldo_pk(clave))


# MOVIMIENTOS

class DetalleMovimientoPKListAPIView(RetrieveAPIView):
    """ Devuelve un movimiento segun ID y su detalle """

    serializer_class = MovimientoSerializer

    def get_queryset(self):
        return (Movimiento.objects.all())


class RegistrarMovimientoUpdateAPIView(CreateAPIView):
    """ Registar nuevo movimiento y realizar operaciones """
    
    serializer_class = RegistrarMovimientoSerializer
    
    def get_queryset(self):
        
        return (MovimientoDetalle.objects.all())


class EliminarMovimientoDetroyAPIView(RetrieveDestroyAPIView):
    """ Elimina movimiento y restable saldo """
    
    serializer_class = EliminaMovimientoSerializer
    queryset = Movimiento.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        """ Se reformula Destroy para poder restaurar el saldo de las transacciones """
        instance = self.get_object()
        id_mov = instance.id
        id_persona = instance.cliente.id
        
        recuperado = MovimientoDetalle.objects.RecuperaImporteTransaccion(id_mov)
        Cuenta.objects.RestauraSaldo(id_persona, recuperado)

        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)