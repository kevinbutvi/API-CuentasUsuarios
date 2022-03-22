from dataclasses import fields
from pyexpat import model
from traceback import print_tb
from urllib import request
from rest_framework import serializers, pagination
from .models import (
    Cliente,
    Movimiento,
    MovimientoDetalle,
    Cuenta,
    
)

import requests, urllib, json

#
from drf_writable_nested import WritableNestedModelSerializer



class ClienteSerializer(serializers.ModelSerializer):
    """ Serializer para la creacion de un nuevo Cliente """
    
    class Meta:
        model = Cliente
        fields = (
            "nombre",
            )

    def create(self, validated_data):
        """ Se crea el cliente y automaticamente se crea la cuenta asociada """
        
        nombre_cliente = validated_data["nombre"]
        inst = Cliente.objects.get_or_create(
            nombre = nombre_cliente,
        )
        inst_cliente = Cliente.objects.get(
            nombre = nombre_cliente,
        )
        instancia = Cuenta.objects.create(
            cliente = inst_cliente,
            saldo_disponible = 0,
        )
        return(inst_cliente)


class Paginador(pagination.PageNumberPagination):
    """ Serializer para Registros """
    
    page_size = 5 # Bloque de registros por pagina
    max_page_size = 50 # Bloque de registros en memoria
    

class MovimientoClienteSerializer(serializers.ModelSerializer):
    """ Serializer de Movimientos """
    cliente = ClienteSerializer()
    
    class Meta:
        model = Movimiento
        fields = (
            "id",
            "fecha",
            "cliente"
        )


class MovimientoDetalleSerializer(serializers.ModelSerializer):
    """ Serializer para Mostrar detalles de Movimientos """
    
    movimiento = MovimientoClienteSerializer()
    
    class Meta:
        model = MovimientoDetalle
        fields = (
            "tipo",
            "importe",
            "movimiento",
        )


class MovimientoSerializer1(serializers.ModelSerializer):
    """ Serializer para Movimiento """
    
    class Meta:
        model = Movimiento
        fields = ("__all__")


class MovimientoSerializer(serializers.ModelSerializer):
    """ Serializer de Movimientos """
    cliente = ClienteSerializer()
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Movimiento
        fields = (
            "fecha",
            "cliente",
            "total",
        )
    
    def get_total(self, obj):
        """ Suma total de todos los detalles de ese movimiento """
        total = MovimientoDetalle.objects.total_movimientos(obj.id)
        return(total)


class ClienteSaldoSerializer(serializers.ModelSerializer):
    """ Serializer para Clientes y Saldos """
    cliente = ClienteSerializer()

    class Meta:
        model = Cuenta
        fields = (
            "cliente",
            "saldo_disponible",
        )


class ClienteSaldoUSDSerializer(serializers.ModelSerializer):
    """ Serializer para Clientes y Saldos """
    cliente = ClienteSerializer()
    total_usd = serializers.SerializerMethodField()

    class Meta:
        model = Cuenta
        fields = (
            "cliente",
            "saldo_disponible",
            "total_usd",
        )
        
    def get_total_usd(self, obj):
        """ Dolariza Saldo a DOLAR OFICIAL """

        r = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
        data = r.json()
        valor_dolar = data[0]["casa"]["venta"]
        valor_dolar = valor_dolar.replace(",",".")
        return((obj.saldo_disponible) * float(valor_dolar))


class RegistrarMovimientoSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    """ Serializer para registro de Movimientos """
    
    movimiento = MovimientoSerializer1()


    class Meta:
        model = MovimientoDetalle
        fields = (
            "tipo",
            "importe",
            "movimiento",
        )

    def validate_importe(self, importe):
        """ Valida importe y envia a manager para realizar la actualizacion """

        movimiento = self.initial_data["tipo"]
        id = self.initial_data["movimiento.cliente"]
        consulta_saldo = True
        
        if movimiento == "egreso":
            consulta_saldo = Cuenta.objects.valida_operacion(id, importe)

        if consulta_saldo == True:
            Cuenta.objects.modifica_saldo(id, importe, movimiento)
            return (importe)
        else:
            raise serializers.ValidationError("El monto de la trasaccion no puede ser menor al saldo")

    def create(self, validated_data):
        """ Si NO existe movimiento para ese dia y ese usuario lo crea, sigo sigue """
        
        tipo_mov = validated_data["tipo"]
        importe_mov = validated_data["importe"]
        mov_fecha = validated_data["movimiento"]["fecha"]
        mov_cliente = validated_data["movimiento"]["cliente"]
        mov = Movimiento.objects.get_or_create(
            cliente = mov_cliente,
            fecha = mov_fecha,
        )
        inst_mov = Movimiento.objects.get(
            cliente = mov_cliente,
            fecha = mov_fecha,
        )
        instancia = MovimientoDetalle.objects.create(
            tipo = tipo_mov,
            importe = importe_mov,
            movimiento = inst_mov,
        )
        return(instancia)


class EliminaMovimientoSerializer(serializers.ModelSerializer):
    """ Serializer para eliminar un movimiento, su detalle y restaurar saldo """
    
    class Meta:
        model = Movimiento
        fields = ("__all__")