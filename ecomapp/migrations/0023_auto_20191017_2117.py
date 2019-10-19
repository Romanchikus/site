# Generated by Django 2.2.3 on 2019-10-17 18:17

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0022_auto_20191016_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='CreditCardType',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='NameonCard',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='zipcode',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=django_countries.fields.CountryField(max_length=746, multiple=True),
        ),
    ]
