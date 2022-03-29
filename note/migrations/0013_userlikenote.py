# Generated by Django 3.2.12 on 2022-03-29 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0012_usercollectnote'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLikeNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='note.note', verbose_name='note')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='note.user', verbose_name='user')),
            ],
        ),
    ]
