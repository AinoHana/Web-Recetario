# Generated by Django 5.2.4 on 2025-07-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='permitir_mensajes_privados',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='recibir_emails_mensajes_privados',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='recibir_emails_recetas_nuevas',
            field=models.BooleanField(default=True),
        ),
    ]
