# Generated by Django 3.0.3 on 2020-02-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0005_auto_20200212_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='comments',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
