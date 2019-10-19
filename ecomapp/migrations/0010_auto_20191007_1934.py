# Generated by Django 2.2.3 on 2019-10-07 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0009_order_card_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='buying_type',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Accepted for processing', 'Accepted for processing'), ('Performed', 'Performed')], max_length=200),
        ),
    ]