# Generated by Django 5.1.3 on 2024-11-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_rename_pedidos_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='qtd_total',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]