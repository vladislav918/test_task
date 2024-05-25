# Generated by Django 4.2 on 2024-05-25 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places_remember', '0004_remove_coordinates_memory_memory_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memory',
            name='coordinates',
        ),
        migrations.CreateModel(
            name='MemoryCoordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places_remember.coordinates')),
                ('memory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places_remember.memory')),
            ],
        ),
        migrations.AddField(
            model_name='coordinates',
            name='memories',
            field=models.ManyToManyField(through='places_remember.MemoryCoordinates', to='places_remember.memory'),
        ),
    ]