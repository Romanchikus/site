# Generated by Django 3.0.3 on 2020-02-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Performed', 'Performed'), ('Accepted for processing', 'Accepted for processing'), ('Paid', 'Paid')], max_length=200),
        ),
    ]
