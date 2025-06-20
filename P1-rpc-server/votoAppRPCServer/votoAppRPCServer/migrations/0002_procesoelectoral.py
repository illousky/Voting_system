# Generated by Django 4.2.13 on 2025-02-24 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votoAppRPCServer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcesoElectoral',
            fields=[
                ('idProcesoElectoral', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('nombreProcesoElectoral', models.CharField(max_length=128)),
                ('fechaInicio', models.DateTimeField()),
                ('fechaFin', models.DateTimeField()),
            ],
            options={
                'db_table': 'proceso_electoral',
            },
        ),
    ]
