# Generated by Django 2.2.3 on 2019-10-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0008_auto_20191006_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='card_number',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
