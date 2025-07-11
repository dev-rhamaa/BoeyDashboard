# Generated by Django 5.2.4 on 2025-07-11 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(help_text='Timestamp embedded in the MQTT payload')),
                ('sensor_id', models.CharField(max_length=100)),
                ('ph', models.FloatField(help_text='pH value of the water')),
                ('turbidity_ntu', models.FloatField(help_text='Turbidity (NTU)')),
                ('do_mg_l', models.FloatField(help_text='Dissolved oxygen (mg/L)')),
                ('ec_us_cm', models.FloatField(help_text='Electrical conductivity (µS/cm)')),
                ('temperature_c', models.FloatField(help_text='Water temperature (°C)')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('received_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.DeleteModel(
            name='SensorData',
        ),
    ]
