# Generated by Django 2.1b1 on 2018-07-12 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Amazonapp', '0006_auto_20180712_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
