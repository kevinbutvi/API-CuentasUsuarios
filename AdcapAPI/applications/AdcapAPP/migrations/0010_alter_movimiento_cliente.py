# Generated by Django 4.0.3 on 2022-03-21 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdcapAPP', '0009_alter_movimiento_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='AdcapAPP.cliente'),
        ),
    ]