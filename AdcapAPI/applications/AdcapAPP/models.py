from model_utils.models import TimeStampedModel
#
from django.db import models

from .managers import MovimientoManager, CuentaManager, MovimientoDetalleManager


class Cliente(TimeStampedModel):
    """ Modelo para Clientes """
    
    nombre = models.CharField("Nombre", max_length=80, unique=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return (str(self.id) + " - " + str(self.nombre))


class Cuenta(TimeStampedModel):
    """ Modelo para Cuenta-Cliente """
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, unique=True, related_name="cuenta_cliente")
    saldo_disponible = models.FloatField(default=0)
    
    objects = CuentaManager()
    
    class Meta:
        verbose_name = "Cuenta "
        verbose_name_plural = "Cuentas"
    
    def __str__(self):
        return (str(self.id) + " - " + str(self.cliente.nombre) + ' - ' + str(self.saldo_disponible))


class Movimiento(TimeStampedModel):
    """ Modelo para Movimientos """
    
    fecha = models.DateField("Fecha de Movimiento", auto_now=False, auto_now_add=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="movimientos")
    
    objects = MovimientoManager()
    
    class Meta:
        verbose_name = "Movimiento "
        verbose_name_plural = "Movimientos"
    
    def __str__(self):
        return (str(self.id) + " - " + str(self.cliente.nombre) + '-' + str(self.fecha))


class MovimientoDetalle(TimeStampedModel):
    """ Modelo para Detalles de Movimientos """
    movimiento_choices = [
        ("ingreso", "Ingreso"),
        ("egreso", "Egreso")
    ]
    
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name="movimiento")
    tipo = models.CharField("Tipo de Movimiento", max_length=30, choices=movimiento_choices, default="Ingreso")
    importe = models.FloatField()
    
    objects = MovimientoDetalleManager()
    
    class Meta:
        verbose_name = "Detalle_Movimiento"
        verbose_name_plural = "Detalles_Movimientos"
    
    def __str__(self):
        return (str(self.id) + " - " + str(self.tipo) + ' - ' + str(self.importe) + " - " + str(self.movimiento.cliente.nombre))
