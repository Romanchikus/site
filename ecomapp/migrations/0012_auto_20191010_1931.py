# Generated by Django 2.2.3 on 2019-10-10 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0011_auto_20191007_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='card_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted for processing', 'Accepted for processing'), ('Performed', 'Performed'), ('Paid', 'Paid')], max_length=200),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='images', to='ecomapp.Product')),
            ],
        ),
    ]