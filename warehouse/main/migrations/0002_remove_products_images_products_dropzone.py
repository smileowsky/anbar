# Generated by Django 5.0.2 on 2024-03-06 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='images',
        ),
        migrations.AddField(
            model_name='products',
            name='dropzone',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
