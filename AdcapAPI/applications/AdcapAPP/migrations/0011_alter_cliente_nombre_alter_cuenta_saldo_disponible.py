# Generated by Django 4.0.3 on 2022-03-21 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdcapAPP', '0010_alter_movimiento_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=80, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='saldo_disponible',
            field=models.FloatField(default=0),
        ),
    ]