# Generated by Django 3.0.3 on 2020-07-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0006_auto_20200727_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Performed', 'Performed'), ('Paid', 'Paid'), ('Accepted for processing', 'Accepted for processing')], max_length=200),
        ),
    ]
