# Generated by Django 2.0.1 on 2019-09-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Goods', '0004_auto_20190910_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfomodel',
            name='commodityinfo',
            field=models.CharField(max_length=200, verbose_name='商品说明'),
        ),
    ]
