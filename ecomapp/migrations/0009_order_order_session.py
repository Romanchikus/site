# Generated by Django 3.0.3 on 2020-09-19 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0008_auto_20200919_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_session',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]