# Generated by Django 2.0.6 on 2018-07-10 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amazonapp', '0003_cart1'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart1',
            name='subtotal',
            field=models.IntegerField(default=0),
        ),
    ]
