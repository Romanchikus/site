# Generated by Django 2.2.3 on 2019-10-10 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0014_auto_20191010_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Performed', 'Performed'), ('Accepted for processing', 'Accepted for processing'), ('Paid', 'Paid')], max_length=200),
        ),
    ]