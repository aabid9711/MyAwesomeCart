# Generated by Django 3.1.4 on 2020-12-29 12:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201229_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdates',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='zipCode',
        ),
        migrations.AddField(
            model_name='order',
            name='zipcode',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
