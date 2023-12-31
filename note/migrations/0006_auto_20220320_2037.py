# Generated by Django 3.2.12 on 2022-03-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0005_auto_20220320_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='pic1.jpg', null=True, upload_to='avatar', verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=11, null=True, unique=True),
        ),
    ]
