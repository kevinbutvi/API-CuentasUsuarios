from django.contrib import admin

from .models import *

# Register your models here.



admin.site.register(Cliente)
admin.site.register(Cuenta)
admin.site.register(Movimiento)
admin.site.register(MovimientoDetalle)