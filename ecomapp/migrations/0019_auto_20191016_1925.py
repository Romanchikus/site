# Generated by Django 2.2.3 on 2019-10-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0018_auto_20191016_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Performed', 'Performed'), ('Accepted for processing', 'Accepted for processing')], max_length=200),
        ),
    ]
