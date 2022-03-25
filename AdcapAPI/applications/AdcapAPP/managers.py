from time import process_time_ns
from django.db import models
from django.db.models import Sum

# Movimiento_Detalle
class MovimientoDetalleManager(models.Manager):
    """ Manager para el Modelo MovimientoDetalle """
    def mov_detalle(self, pk):
        """ Busca el detalle de un movimiento segun ID """
        existe = self.filter(movimiento__id = pk).exists()
        if existe:
            return(self.filter(movimiento__id = pk))
        else:
            return (self)

    def total_movimientos(self, id_mov):
        """ Suma todos los detalles de ese movimiento """
        tot_obj = self.filter(movimiento__id = id_mov).aggregate(Sum("importe"))
        return(tot_obj["importe__sum"])
    
    def RecuperaImporteTransaccion(self, id_mov):
        """ Recupera importe de transaccion para restaurar """

        tot_recuperado = { 
            "ingreso" : self.filter(movimiento__id = id_mov, tipo = "ingreso").aggregate(Sum("importe")),
            "egreso" : self.filter(movimiento__id = id_mov, tipo = "egreso").aggregate(Sum("importe"))
            }
        return(tot_recuperado)


# Movimiento
class MovimientoManager(models.Manager):
    """ Manager para el Modelo Movimiento"""


# Cuenta
class CuentaManager(models.Manager):
    """ Manager para el modelo Cuenta """

    def saldo_pk(self, pk):
        """ Busca el cliente que se envia desde el queryset que a su vez la recibe por URL"""
        resultado = self.filter(cliente__id = pk)
        return (resultado)

    def valida_operacion(self, id, monto):
        """ Valida que saldo no sea menos de lo que se quiere transferir """
        resultado = self.filter(
            cliente__id = id,
            saldo_disponible__gte = monto
            )
        if resultado:
            return(True)
        else:
            return(False)

    def modifica_saldo(self, id, importe, movimiento ):
        """ Actualiza saldo de la cuenta del cliente """
        saldo = self.filter(cliente__id = id).values("saldo_disponible").first()
        saldo_disp = saldo["saldo_disponible"]
        if movimiento == "egreso":
            self.filter(
                cliente__id = id,
                ).update(saldo_disponible = saldo_disp - importe)
        else:
            if movimiento == "ingreso":
                self.filter(
                cliente__id = id,
                ).update(saldo_disponible = saldo_disp + importe)
        return(importe)

    def RestauraSaldo(self, id, recuperado):
        """ Restaura saldo en cuenta luego de un destroy """
        saldo = self.filter(cliente__id = id).values("saldo_disponible").first()
        saldo_disp = saldo["saldo_disponible"]
        if (recuperado["egreso"]["importe__sum"]  != None):
            egreso = recuperado["egreso"]["importe__sum"]
        else:
            egreso = 0
        if (recuperado["ingreso"]["importe__sum"] != None):
            ingreso = recuperado["ingreso"]["importe__sum"]
        else:
            ingreso = 0
        
        self.filter(cliente__id = id,).update(saldo_disponible = saldo_disp + egreso - ingreso)
        return (recuperado)
