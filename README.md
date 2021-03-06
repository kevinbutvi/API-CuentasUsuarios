# API-CuentasUsuarios
Challenge, API de gestion de usuarios y cuentas bancarias


Crear una API REST que brinde la siguiente funcionalidad básica de un sistema de control de movimientos monetarios. El mismo debe permitir crear y editar ingresos y egresos de dinero, y mostrar un balance resultante de las operaciones registradas.

Requerimientos Técnicos:
• Deberás desarrollar una API REST utilizando FastAPI
• Los datos mostrados deben ser persistidos en una base de datos relacional
• La API deberá exponer endpoints que devuelvan datos en JSON
El sistema debe tener los modelos Cliente, Movimiento, MovimientoDetalle y Cuenta con los siguientes atributos:

Cliente
- id PK
- nombre [string]

Cuenta
- cliente [Cliente]
- saldo_disponible [float]

Movimiento
- id PK
- fecha [datetime]
- cliente [Cliente]

MovimientoDetalle
- movimiento [Movimiento]
- tipo [string]
- importe [float]

La misma debe proporcionar los siguientes endpoints:
Clientes
• Registrar/Editar un cliente
• Eliminar un cliente
• Consultar un cliente
• Listar todos los clientes

Movimientos
• Registrar un movimiento. Debe actualizar el saldo disponible de la cuenta correspondiente al cliente que realiza la transacción, dependiendo del tipo de movimiento el saldo puede ser aumentado o disminuido.
• Eliminar un movimiento. Restaura saldo disponible del cliente.
• Consultar un movimiento y su detalle.

Saldos
• Consultar saldo disponible en cuenta del cliente.
Por otro lado, deben existir los siguientes métodos:
• La clase Movimiento debe exponer un método get_total el cual calcule el importe total del movimiento y retorne ese valor en el serializer correspondiente.
• La clase Cuenta debe exponer el método get_total_usd que valorice el saldo disponible en dólares utilizando la cotización expuesta en la API de https://www.dolarsi.com/api/api.php?type=valoresprincipales, “Dolar Bolsa" y retorne el valor en el serializer correspondiente.


-------------------------------

Consideraciones finales:
• Tené en cuenta que existen dos tipos diferentes de movimientos. Ingreso (impacto positivo en saldo disponible) y Egreso (impacto negativo en saldo disponible).
• Al crear un movimiento de tipo Egreso se debe validar que haya suficiente saldo disponible en la cuenta del cliente, en caso de no contar con saldo suficiente se debe retornar un error de validación.
• No debe ser posible modificar el tipo de operación (Ingreso o Egreso) una vez creada.
• Implementar test unitario para validar los endpoints.
• El código fuente debe ser subido a un repositorio público, el cual debe ser proporcionado para su correcta examinación.
